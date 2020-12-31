"""test_front_end

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""

from flask import url_for
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
import pytest


@pytest.mark.front_end
@pytest.mark.usefixtures('live_server')
class TestFrontEnd:

    ALL_FIELDS = ('delimiter', 'quote_character', 'include_header', 'root_node', 'template',
                  'is_nested', 'key_separator', 'exclude_null', 'table_name')

    @staticmethod
    def clear_field(webdriver: WebDriver, element_id: str):
        """Click download button

        :param WebDriver webdriver: Selenium webdriver
        :param str element_id: Element id
        """

        webdriver.find_element_by_id(element_id).clear()

    @staticmethod
    def click_button(webdriver: WebDriver, element_id: str):
        """Click button

        :param WebDriver webdriver: Selenium webdriver
        :param str element_id: Element id
        """

        webdriver.find_element_by_id(element_id).click()

    @staticmethod
    def get_index_page(webdriver: WebDriver):
        """Navigate to main page

        :param WebDriver webdriver: Selenium webdriver
        """

        webdriver.get(url_for('index', _external=True))

    @staticmethod
    def verify_field_invalid(webdriver: WebDriver, element_id: str):
        """Verifies that field is marked as invalid

        :param WebDriver webdriver: Selenium webdriver
        :param str element_id: Element id
        """

        assert 'is-invalid' in webdriver.find_element_by_id(element_id).get_attribute('class')

    @staticmethod
    def verify_invalid_feedback_visible(webdriver: WebDriver, element_id: str):
        """Verifies that invalid feedback for field is visible

        :param WebDriver webdriver: Selenium webdriver
        :param str element_id: Element id
        """

        selector = f'//*[@id="{element_id}"]/following-sibling::div[@class="invalid-feedback"]'
        assert webdriver.find_element_by_xpath(selector).is_displayed()

    @pytest.mark.parametrize('field', ('schema', 'num_rows'))
    def test_field_required(self, selenium: WebDriver, field: str):
        """Test to ensure required fields displays errors if missing

        :param WebDriver selenium: Selenium webdriver instance
        :param str field: Field element id
        :raises: AssertionError
        """

        # Given the user is on the main page
        self.get_index_page(selenium)

        # And the specified field is empty
        self.clear_field(selenium, field)

        # When the user clicks the download button
        self.click_button(selenium, 'downloadData')

        # Then the specified field should highlight red
        self.verify_field_invalid(selenium, field)

        # And the field should display an error message
        self.verify_invalid_feedback_visible(selenium, field)

    def test_column_name_required(self, selenium: WebDriver):
        """Test to ensure required fields displays errors if missing

        :param WebDriver selenium: Selenium webdriver instance
        :raises: AssertionError
        """

        # Given the user is on the main page
        self.get_index_page(selenium)

        # When the user clicks the download button
        self.click_button(selenium, 'addField')
        self.click_button(selenium, 'downloadData')

        # Then the specified field should highlight red
        assert 'is-invalid' in selenium.find_elements_by_xpath('//input[@name="name"]')[-1].get_attribute('class')

    @pytest.mark.parametrize('file_format,visible_fields', (
            ('CSV', ('delimiter', 'quote_character', 'include_header')),
            ('TSV', ('delimiter', 'quote_character', 'include_header')),
            ('XML', ('root_node',)),
            ('HTML', ('template',)),
            ('JSON', ('is_nested', 'key_separator', 'exclude_null')),
            ('SQL', ('table_name',))
    ))
    def test_format_additional_options(self, selenium: WebDriver, file_format: str, visible_fields: tuple):
        """Test to ensure changing file format updates additional options

        :param WebDriver selenium: Selenium webdriver instance
        :param str file_format: File format
        :param tuple visible_fields: Visible fields
        :raises: AssertionError
        """

        # Given the user is on the main page
        self.get_index_page(selenium)

        # When the user changes the file format
        file_format_selector = Select(selenium.find_element_by_id('file_format'))
        file_format_selector.select_by_visible_text(file_format)

        # The appropriate fields should display
        for field in visible_fields:
            assert selenium.find_element_by_id(field).is_displayed()

        # And all other fields should not display
        for field in set(self.ALL_FIELDS) - set(visible_fields):
            assert not selenium.find_element_by_id(field).is_displayed()

    def test_remove_column(self, selenium: WebDriver):
        """Test to columns can be removed

        :param WebDriver selenium: Selenium webdriver instance
        :raises: AssertionError
        """

        # Given the user is on the main page
        self.get_index_page(selenium)

        # When the user removes the last column
        selenium.find_elements_by_xpath('//div[contains(@onclick, "removeColumn")]')[-1].click()

        # Then the last column should be removed
        columns = [item.get_attribute("value") for item in selenium.find_elements_by_xpath('//input[@name="name"]')]
        assert "Gender" not in columns
