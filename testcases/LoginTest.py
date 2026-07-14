import allure
import pytest

from pages.LoginPage import LoginPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider

_login_data = dataProvider.get_data("Sheet1")
_login_ids = [f"{row[0]}-{row[1]}-{row[2]}" for row in _login_data]


class TestLoginTest(BaseTest):
    @pytest.mark.dependency(name="login")
    @pytest.mark.parametrize(("LoginID", "Firm", "Location", "Password"), _login_data, ids=_login_ids)
    def test_login(self, page, LoginID, Firm, Location, Password):
        allure.dynamic.parameter("Password", Password, mode=allure.parameter_mode.MASKED)
        with allure.step("*******Executing Login Test********"):
            returns_page = LoginPage(page)\
                .do_login(LoginID, Firm, Location, Password)\
                .select_createReturn()
            returns_page.verify_element_visible("create_return_btn")







