# Insurance Claim Processing System (Fixed)

This is a fixed version of the demo project that previously crashed when a policy
was in `grace_period` with `grace_period_days = 0`.

See `FIX_SUMMARY.md` for details on the bug, root cause, and the fix applied.

## How to run

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run tests:

```powershell
pytest -v
```

Run demo:

```powershell
python demo.py
```
