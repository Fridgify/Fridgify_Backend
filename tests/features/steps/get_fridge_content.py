from behave import *

use_step_matcher("re")


@given("user is authenticated for fridge")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@step("fridge is not empty")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@when('user is navigates to "Content Overview"-Page')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@then("load all items")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@step("show items")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@given("user is not authenticated for fridge")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@when('user navigates to "Content Overview"-Page')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@then('redirect to "Fridges Overview"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@step("send error message")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@given("user is authenticated")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@step("fridge is empty")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@then("show empty list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@step("show add item \(manually and via scanning\) button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")


@step('show text -> "Fridge is currently empty"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print("step")
