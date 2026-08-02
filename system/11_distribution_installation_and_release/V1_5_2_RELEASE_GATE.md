# V1.5.2 Release Gate

Status: pre-C4 gate. No unchecked item is a release or runtime-adoption claim.

- [ ] Create and review an exact candidate commit from this source scope.
- [ ] Pass the full local suite with zero Framework integration skips.
- [ ] Pass Windows, Ubuntu, and macOS CI for that exact candidate commit.
- [ ] Reconfirm public-material, rights, privacy, secret, dependency, and
      exact Framework `v0.2.0` review evidence.
- [ ] Review the protected-main merge commit separately.
- [ ] Verify that `v1.5.2` is unused, then create and verify an annotated tag
      pointing to that exact commit before any GitHub Release exists.
- [ ] Create and inspect a draft GitHub Release using that exact existing tag,
      reviewed notes, and zero uploaded assets.
- [ ] Obtain separate accountable-human C4-Publish approval for that exact
      inspected draft.
- [ ] Publish the approved draft without changing its tag, notes, or assets.
- [ ] Verify the immutable Release, annotated tag, generated source archives,
      and current public identity after publication.

Local source validation, public release, and local controlled adoption remain
separate actions.
