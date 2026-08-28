from __future__ import annotations

from pathlib import Path

import pytest

import pyxis.ui.first_changed_basis_root_backed_handoff_research_session_shell as handoff_module
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _session,
)


def test_44h_runner_chains_exact_explicit_handoff_into_existing_root_backed_shell(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, ordinary_reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44h-runner-member")
    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, handoff, _, _, _ = _persist_valid_overlay(root_dir, stem="44h-runner")
    observed: dict[str, object] = {}

    class Fake44HShell:
        def run(self):
            observed["44h_run"] = True
            return handoff

    class FakeRootBackedShell:
        def run(self):
            observed["receiver_run"] = True
            return None

    def fake_create_44h(reentry, appended_items):
        observed["ordinary_reentry"] = reentry
        observed["appended_items"] = tuple(appended_items)
        return Fake44HShell()

    def fake_create_receiver(reentry):
        observed["receiver_reentry"] = reentry
        return FakeRootBackedShell()

    monkeypatch.setattr(
        handoff_module,
        "create_first_changed_basis_root_backed_handoff_research_session_shell",
        fake_create_44h,
    )
    monkeypatch.setattr(
        handoff_module,
        "create_root_backed_research_session_shell",
        fake_create_receiver,
    )

    returned = handoff_module.run_first_changed_basis_root_backed_handoff_research_session_shell(
        ordinary_reentry,
        (member,),
    )

    assert returned is handoff
    assert observed["44h_run"] is True
    assert observed["ordinary_reentry"] is ordinary_reentry
    assert observed["appended_items"] == (member,)
    assert observed["receiver_reentry"] is handoff
    assert observed["receiver_run"] is True


def test_44h_runner_normal_close_launches_nothing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, ordinary_reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44h-runner-close")
    observed = {"receiver": 0}

    class Fake44HShell:
        def run(self):
            return None

    monkeypatch.setattr(
        handoff_module,
        "create_first_changed_basis_root_backed_handoff_research_session_shell",
        lambda reentry, appended_items: Fake44HShell(),
    )

    def fail_receiver(reentry):
        observed["receiver"] += 1
        raise AssertionError("normal close must not launch the root-backed receiver")

    monkeypatch.setattr(
        handoff_module,
        "create_root_backed_research_session_shell",
        fail_receiver,
    )

    assert (
        handoff_module.run_first_changed_basis_root_backed_handoff_research_session_shell(
            ordinary_reentry,
            (member,),
        )
        is None
    )
    assert observed["receiver"] == 0


def test_44h_runner_rejects_untyped_shell_return_before_receiver_launch(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, ordinary_reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44h-runner-invalid")
    observed = {"receiver": 0}

    class Fake44HShell:
        def run(self):
            return object()

    monkeypatch.setattr(
        handoff_module,
        "create_first_changed_basis_root_backed_handoff_research_session_shell",
        lambda reentry, appended_items: Fake44HShell(),
    )

    def fail_receiver(reentry):
        observed["receiver"] += 1
        raise AssertionError("invalid handoff must not reach the receiver")

    monkeypatch.setattr(
        handoff_module,
        "create_root_backed_research_session_shell",
        fail_receiver,
    )

    with pytest.raises(TypeError, match="invalid root-backed handoff"):
        handoff_module.run_first_changed_basis_root_backed_handoff_research_session_shell(
            ordinary_reentry,
            (member,),
        )
    assert observed["receiver"] == 0
