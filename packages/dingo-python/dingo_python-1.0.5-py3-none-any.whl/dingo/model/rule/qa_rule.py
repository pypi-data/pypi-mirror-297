import re
import string
import jieba
import langid
import textstat
import wordninja

from typing import List, Tuple
from hanziconv import HanziConv
from nltk.tokenize import WordPunctTokenizer

from dingo.model.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.model.rule.common.detect_lang import decide_language_by_str
from dingo.model.rule.common.util import (normalize, base_rps_frac_chars_in_dupe_ngrams, get_stop_words,
                                          split_paragraphs, TextSlice, Extractor, delete_punc_en, delete_punc_ch,
                                          get_tokens, is_sha256)
from dingo.config.config import DynamicRuleConfig
from dingo.io import MetaData


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaOnlyUrl(BaseRule):
    """check whether content is only an url link."""
    custom_config = DynamicRuleConfig(pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        SEARCH_REGEX = re.compile(cls.custom_config.pattern)
        content_without_url = SEARCH_REGEX.sub("", input_data.content)
        if len(content_without_url.strip()) == 0:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Content is only an url link.'
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', [])
class QaChaosEnLine(BaseRule):
    """check whether content has english garbled characters at the line level."""
    custom_config = DynamicRuleConfig(file_path = '')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        language = decide_language_by_str(content)
        if language != 'en':
            return res
        for content_line in content.split("\n"):
            if len(content_line.strip()) == 0:
                continue
            af_en = delete_punc_en(content_line)
            af_ch = delete_punc_ch(af_en)
            str_len = len(af_ch)
            seg_len = len(list(jieba.cut(af_ch)))
            if seg_len == 0:
                continue
            if str_len / seg_len < 1.2:
                res.error_status = True
                res.error_type = 'QUALITY_INEFFECTIVENESS'
                res.error_name = cls.__name__
                res.error_reason = content_line
                return res
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', [])
class QaChaosZh(BaseRule):
    """check whether content has chinese garbled characters."""
    custom_config = DynamicRuleConfig(file_path = '', pattern = r'[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+(""|[\n\s])')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        language = decide_language_by_str(content)
        if language != 'zh':
            return res
        af_en = delete_punc_en(content)
        af_ch = delete_punc_ch(af_en)
        text = re.sub(cls.custom_config.pattern, "", af_ch)
        simplified_text = HanziConv.toSimplified(text)
        seg_len = len(list(jieba.cut(simplified_text)))
        str_len = len(text)
        if str_len == 0 or seg_len == 0 and get_tokens(content, language) < 50:
            return res
        if str_len / seg_len > 1.2:
            return res
        else:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Content has chinese garbled characters.'
            return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaEnterMore(BaseRule):
    """check whether content has 8 consecutive carriage returns."""
    custom_config = DynamicRuleConfig(key_list=[r"\n{8,}", r"\r\n{8,}"])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        for p in cls.custom_config.key_list:
            SEARCH_REGEX = re.compile(p)
            match = SEARCH_REGEX.search(content)
            if match:
                res.error_status = True
                res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
                res.error_name = cls.__name__
                res.error_reason = 'Content has 8 consecutive carriage returns.'
                return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaSpaceMore(BaseRule):
    """check whether content has 500 spaces."""
    custom_config = DynamicRuleConfig(pattern=" {500,}")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        SEARCH_REGEX = re.compile(cls.custom_config.pattern)
        match = SEARCH_REGEX.search(content)
        if match:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = 'Content has 500 spaces.'
            return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaEnterRatioMore(BaseRule):
    """check whether the number of enter / the number of content > 25%"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        if len(content) == 0:
            return res

        ratio = content.count("\n") / len(content)
        if ratio > 0.25:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = 'The number of enter / the number of content > 25%.'
            return res
        return res


@Model.rule_register('QUALITY_DISFLUENCY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaWordStuck(BaseRule):
    """check whether words are stuck."""
    custom_config = DynamicRuleConfig(
        key_list=[
            r"https?://[^\s]+|www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            r"\.pdf$",
            r"\w+\.bat",
            r"(\/.*\/.*)",
            r"[01]+|[0-7]+|0x[0-9a-fA-F]+"
        ]
    )

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        language = decide_language_by_str(content)
        if language != 'en':
            return res

        for p in cls.custom_config.key_list:
            content = re.sub(p, "", content)
        word_list = [
            word.strip(string.punctuation) for word in
            re.split(r"[⁃>#%-.—,–!?;:\s|_/   =\\@\((.*?)\)\[(.*?)\]]\s*", content)
        ]
        for longest_string in word_list:
            if len(longest_string) > 45 and is_sha256(longest_string) == False:
                lan = decide_language_by_str(longest_string)
                cut = wordninja.split(longest_string)
                if lan == "en" and len(cut) > 1:
                    res.error_status = True
                    res.error_type = 'QUALITY_DISFLUENCY'
                    res.error_name = cls.__name__
                    res.error_reason = str(longest_string)
                    return res
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaImgOrHtml(BaseRule):
    """check whether content has image links or html tags."""
    custom_config = DynamicRuleConfig(pattern=r"(<img[^>]*>)|<p[^>]*>(.*?)<\/p>|<o:p[^>]*>(.*?)<\/o:p>")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = re.findall(cls.custom_config.pattern, content)
        if matches:
            res.error_status = True
            res.error_type = 'QUALITY_IRRELEVANCE'
            res.error_name = cls.__name__
            res.error_reason = 'Content has image links or html tags: ' + ','.join(matches)
            return res
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaInvisibleChar(BaseRule):
    """check whether content has invisible chars."""
    custom_config = DynamicRuleConfig(pattern=r"[\u2000-\u200F\u202F\u205F\u3000\uFEFF\u00A0\u2060-\u206F\uFEFF\xa0]")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = re.findall(cls.custom_config.pattern, content)
        if matches:
            res.error_status = True
            res.error_type = 'QUALITY_IRRELEVANCE'
            res.error_name = cls.__name__
            res.error_reason = 'Content has invisible chars: ' + ','.join(matches)
            return res
        return res

if __name__ == '__main__':
    content = """Outline a basic business model for an online grocery delivery service. Be as detailed and concise as possible, and limit your response to 500 words:", "content": " \n\nTitle: \"Fresh Food Delivered - The Online Grocery Delivery Service\"\n\nI. Introduction\nThe Fresh Food Delivered business model is designed to provide a streamlined and seamless grocery shopping experience for urbanites. The primary target market comprises millennials and busy working professionals who want the ease of online grocery shopping, along with the assurance of fresh and high-quality products delivered right to their doorstep. Our platform will offer a wide range of products from local and national grocery stores, ensuring that customers have access to their favorite brands and products.\n\nII. Business Strategy\n\n1. Online Ordering and Payment Platform \n\nCustomers can conveniently shop for groceries directly on our platform using an intuitive and user-friendly interface. We provide an easy comparison option for pricing, quality, and freshness of products. Payment can be done using major credit card or digital wallets for secure online transaction.\n\n2. Partnership with Local and National Grocery Stores\n\nFresh Food Delivered will partner with major grocery store chains and local markets, ensuring that a broad range of products, including fresh produce, meats, dairy, pantry staples, and household essentials, are available for purchase. \n\n3. In-house Freshness Guarantee\n\nThe delivery time will be within 24 hours to ensure the freshest possible produce. We partner with local suppliers and implement a rigorous quality control process to guarantee the freshness and quality of our products.\n\n4. Flexible Delivery Options\n\nWe provide flexible delivery options such as morning, afternoon, or evening delivery and an option for same-day delivery for time-sensitive orders. \n\n5. Subscription Plans and Discounts\n\nCustomers can opt for subscription-based plans, which offer discounts and regular grocery deliveries. This is ideal for customers who regularly shop at Fresh Food Delivered and want to save on their grocery bills.\n\n6. User Ratings and Reviews\n\nCustomers can rate and review the products and our delivery service. This helps both the customers and the grocery delivery service to improve continuously.\n\n7. Customer Care and Support\n\nWe have a 24/7 customer helpline for any queries, requests or emergencies concerning your order.\n\n8. Referral Program\n\nCustomers can earn rewards like discounts or grocery credits by referring their friends or family members to use the service.\n\nIII. Monetization \n\nFresh Food Delivered will earn revenue from the following sources: \n1. Online grocery sales\n2. Subscriptions\n3. Partnership with grocery stores (Commission)\n4. Referral marketing\n\nIV. Operational Requirements\n\n1. Website/ Mobile Application Development\n2. Partnerships with Grocery Stores and Suppliers\n3. Logistics Management System\n4. Warehousing Facility\n5. Customer Service and Support Team\n6. Marketing and Sales Team\n\nV. Financial Analysis\n\nThe financial viability of the business model will depend on factors such as initial investment, ongoing operational expenses, sales volume, and profit margins. It is anticipated that as the market expands with increasing customer demand and positive customer referrals, Fresh Food Delivered will become profitable and self-sustaining.\n\nVI. Risk and Challenges\n\nPotential risks and challenges include:\n1. Competition from other grocery delivery services \n2. Logistics and delivery issues\n3. Customer service and quality control\n4. Technology challenges (website, applications)\n5. Financial risk\n\nVII. Conclusion \n\nFresh Food Delivered’s business model provides a modern and convenient grocery delivery service, aiming to enhance customers' overall shopping experience. By offering fresh products from reliable suppliers, flexible delivery options and competitive pricing, we anticipate to gain market traction and long-term customer loyalty."""
    data = MetaData(
        data_id = '',
        prompt = '',
        content = content
    )
    tmp = QaChaosEnLine().eval(data)
    print(tmp)

