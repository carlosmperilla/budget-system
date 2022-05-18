"""This module handles the translations of the budget system."""

from typing import Dict, List, Tuple

from ..validators.Date import import_months_by_lang
from ..settings.LanguagesText import generate_lang_texts

from ..budget_system import Budget


class SupportLanguage:
    """Class that allows to maintain the budget system compatibility with other languages,
    not available by default.
    """

    def __init__(self,
                new_lang:str,
                months:List[str],
                sections:Dict[str, Dict[str, str]],
                config_file_path:str="",
                current_lang:str="", 
                ) -> None:
        self.new_lang = new_lang
        self.months = months
        self.sections = sections

        self.config_file_path = config_file_path
        self.current_lang = current_lang

    def add_new_lang(self) -> None:
        """This adds a new language, to be used in current and future budgeting systems."""
        import_months_by_lang(self.new_lang, self.months)
        generate_lang_texts(self.new_lang, self.sections)
        
    def translate_to_new_lang(self) -> None:
        """This adds a new language and translates a current budget system."""
        self.add_new_lang()
        Budget.translate_month_folders(self.config_file_path, self.current_lang, self.new_lang)
        print(f"<{self.current_lang}> ==> <{self.new_lang}>")

class FileToLangContext:
    """Class for SupportLanguage for file input support.
    """
    
    @staticmethod
    def clean_str_to_list(string:str, sep:str=",") -> None:
        """This transforms a text string to a list,
        if this string is separated by any characters.
        And it removes the blank spaces to the sides of each element."""
        return [piece.strip() for piece in string.split(sep)]
    
    def __init__(self,lang_file:str) -> None:
        self.lang_file = lang_file

        self.sections_range:Dict[str, Tuple[int, int]] = {
                "Month":(0,2),
                "ShowData":(2,8),
                "BudgetSystem":(8,9),
                "Settings":(9,11)
                }
        self.sections:Dict[str, Dict[str, str]] = {}

    def get_messages(self, unclean_message_list:List[str]) -> Dict[str, str]:
        """This takes a list of messages with their tag and content, 
        returns a dictionary with the tag as the key and its content as the value."""
        messages = {}
        for message in unclean_message_list:
            message_label, message_content = self.clean_str_to_list(message, "=")
            messages[message_label] = message_content
        return messages

    def fill_sections(self, sections_content:List[str]) -> None:
        """This fills sections, segmenting content and parsing it."""
        for section_range in self.sections_range:
            first, limit = self.sections_range[section_range]
            self.sections[section_range] = self.get_messages(sections_content[first:limit])

    def transform(self) -> Tuple[List[str], Dict[str, Dict[str, str]]]:
        """This takes a file with a certain format and transforms it into a tuple
        with months and sections for SupportLanguage.
        """
        with open(self.lang_file, 'r', encoding='utf-8') as l_file:
            months_str, *sections_content  = l_file.readlines()

        months = self.clean_str_to_list(months_str)

        self.fill_sections(sections_content)

        return (months, self.sections)

    def add_new_lang(self, new_lang:str) -> None:
        """This adds a new language, to be used in current and future budgeting systems."""
        months, sections = self.transform()

        support = SupportLanguage(
                                    new_lang=new_lang,
                                    months=months,
                                    sections=sections
                                )
        support.add_new_lang()

    def translate_to_new_lang(self, new_lang:str, config_file_path:str="", current_lang:str="") -> None:
        """This adds a new language and translates a current budget system."""
        months, sections = self.transform()

        support = SupportLanguage(
                                    new_lang=new_lang,
                                    months=months,
                                    sections=sections,
                                    config_file_path=config_file_path,
                                    current_lang=current_lang
                                )
        support.translate_to_new_lang()
