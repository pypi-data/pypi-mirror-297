import pytest

import appl
from appl import Generation, convo, define, gen, need_ctx, ppl, records
from appl.compositor import *


def test_return():
    @ppl
    def func():
        "Hello World"
        return "answer"

    assert func() == "answer"


def test_prompt():
    @ppl
    def func(_ctx):
        "Hello World"
        return records()

    assert str(func()) == "Hello World"


def test_fstring():
    @ppl
    def f1():
        f"a is {1!r}"
        return records()

    assert str(f1()) == f"a is {1!r}"

    @ppl
    def f2():
        f"a is {3.1415:.2f}"
        return records()

    assert str(f2()) == f"a is {3.1415:.2f}"


def test_prompts_change():
    @ppl
    def func():
        "Hello"
        ret1 = records()  # the reference
        ret2 = records().copy()  # the copy of the current prompt
        "World"
        ret3 = records()
        return ret1, ret2, ret3

    ret1, ret2, ret3 = func()
    assert str(ret1) == "Hello\nWorld"
    assert str(ret2) == "Hello"
    assert str(ret3) == "Hello\nWorld"


def test_return_prompt():
    @ppl(default_return="prompt")
    def f1():
        "Hello World"

    assert str(f1()) == "Hello World"

    @ppl(default_return="prompt")
    def f2():
        "Hello World"
        return "answer"

    # The return is unchanged.
    assert str(f2()) == "answer"


def test_record():
    @ppl
    def f2():
        "Hello"
        "World"
        return records()

    @ppl
    def func():
        with NumberedList():
            "first line"
            "second line"
            f2()  # add the prompts from f2, following the current format.
        return records()

    assert str(func()) == f"1. first line\n2. second line\n3. Hello\n4. World"


def test_inner_func():
    @ppl
    def func():
        "Hello"

        def func2():  # the inner function use the same context from the outer function.
            "World"

        func2()
        return records()

    assert str(func()) == "Hello\nWorld"


def test_include_docstring():
    @ppl(include_docstring=True)
    def func():
        """This is a docstring"""
        "Hello"
        return records()

    assert str(func()) == "This is a docstring\nHello"


def test_default_no_docstring():
    @ppl()
    def func():
        """This is a docstring"""
        "Hello"
        return records()

    assert str(func()) == "Hello"


def test_copy_ctx():
    @ppl(ctx="copy")
    def addon():
        "World"
        return str(convo())

    @ppl
    def func2():
        "Hello"
        first = addon()
        second = addon()
        return first, second, records()

    first, second, origin = func2()
    assert first == "Hello\nWorld"
    assert second == "Hello\nWorld"
    assert str(origin) == "Hello"


def test_resume_ctx():
    @ppl(ctx="resume")
    def resume_ctx():
        "Hello"
        return convo()

    target = []
    for i in range(3):
        res = resume_ctx()
        target += ["Hello"]
        assert str(res) == "\n".join(target)


def test_class_resume_ctx():
    class A:
        @ppl(ctx="resume")
        def append(self, msg: str):
            msg
            return convo()

        @classmethod
        @ppl(ctx="resume")
        def append_cls(cls, msg: str):
            msg
            return convo()

    a = A()
    b = A()
    target_a = []
    target_b = []
    target_cls = []
    for i in range(3):
        res = a.append("Hello")
        target_a += ["Hello"]
        assert str(res) == "\n".join(target_a)
        res = b.append("World")
        target_b += ["World"]
        assert str(res) == "\n".join(target_b)
        res = A.append_cls("Class")
        target_cls += ["Class"]
        assert str(res) == "\n".join(target_cls)


def test_class_func():
    class ComplexPrompt:
        def __init__(self, condition: str):
            self._condition = condition

        @ppl(ctx="same")
        def sub1(self):
            if self._condition:
                "sub1, condition is true"
            else:
                "sub1, condition is false"

        @ppl(ctx="same")
        def sub2(self):
            if self._condition:
                "sub2, condition is true"
            else:
                "sub2, condition is false"

        @ppl
        def func(self):
            self.sub1()
            self.sub2()
            return records()

    prompt1 = ComplexPrompt(False).func()
    prompt2 = ComplexPrompt(True).func()
    assert str(prompt1) == "sub1, condition is false\nsub2, condition is false"
    assert str(prompt2) == "sub1, condition is true\nsub2, condition is true"


def test_generation_message():
    appl.init()

    @ppl
    def func():
        "Hello World"
        gen1 = gen(lazy_eval=True)
        "Hi"
        gen2 = gen(lazy_eval=True)
        return gen1, gen2

    gen1, gen2 = func()
    assert str(gen1._args.messages) == "Hello World"
    assert str(gen2._args.messages) == "Hello World\nHi"


def test_generation_message2():
    def fakegen():
        return "24"

    @ppl
    def func():
        f"Q: 1 + 2 = ?"
        f"A: 3"
        f"Q: 15 + 9 = ?"
        f"A: {fakegen()}"
        return convo()

    assert str(func()) == "Q: 1 + 2 = ?\nA: 3\nQ: 15 + 9 = ?\nA: 24"
