# SDK tests in CI (private SDK)

The SRCI SDK must not be published. It is therefore **not** part of this repository or the
package. So that every commit still runs **all** tests, including the SDK-in-the-loop tests, the CI
job `sdk` (`.github/workflows/ci.yml`) works like this:

1. It checks out the SDK from a **private** GitHub repository with a **read-only deploy key**
   (secret `SDK_DEPLOY_KEY`).
2. It builds the simulator library (`srci_py_harness`, Linux `.so` and Windows `.dll`) in the job.
3. It runs `pytest -m sdk` with `SRCI_REQUIRE_SDK=1`: a missing library is an error, the tests are
   never skipped silently.
4. It deletes the SDK from the runner.

## What stays private

The logs of a public repository are public. Therefore:

- The compiler output goes to a file that is not shown. The CMake option `SRCI_SIM_QUIET`
  disables warnings, because warnings quote source lines.
- The pytest output goes to a file. The log shows only counts and the IDs of failed tests
  (`python -m tools.ci_sdk_summary`), never messages, because they can contain SDK log texts.
- No `actions/cache`, no uploaded artifacts: pull requests from forks can read caches.
- The job never runs for pull requests from forks. They do not get secrets anyway, and the job
  has an explicit `if`. `pull_request_target` is not used.
- `persist-credentials: false`: the deploy key is not left in the git configuration.

Run a failed test locally to see details.

## Setup (once)

1. **Create a private repository** on GitHub, e.g. `srci-sdk-private` (Private, no README).
   Check that the license terms of the SDK allow storing it at GitHub.
2. **Push the SDK repository** (the local `SRCI SDK` folder with its private git):

   ```
   cd "D:\Projekte\SRCI\SRCI SDK"
   git remote add origin git@github.com:<owner>/srci-sdk-private.git
   git push -u origin main
   git push origin --tags        # sdk-original = unchanged SDK (baseline of the CUSTOM changes)
   ```

3. **Create a deploy key** (a new key pair, used only for this):

   ```
   ssh-keygen -t ed25519 -C "srci_py-ci" -N "" -f srci_sdk_deploy
   ```

   - `srci-sdk-private` → Settings → Deploy keys → *Add deploy key*: content of
     `srci_sdk_deploy.pub`, **without** "Allow write access".
   - `SRCI_PY` → Settings → Secrets and variables → Actions → *New repository secret*:
     name `SDK_DEPLOY_KEY`, content of `srci_sdk_deploy` (the private key, including the
     BEGIN/END lines).
   - Then delete both files locally.

4. Optional repository **variables** (Settings → Secrets and variables → Actions → Variables):
   - `SDK_REPOSITORY`: if the repository has another name (default `<owner>/srci-sdk-private`).
   - `SDK_REF`: branch, tag or commit of the SDK (default `main`), e.g. to pin an SDK version.
5. Recommended: SRCI_PY → Settings → Actions → General → "Fork pull request workflows":
   *Require approval for all outside collaborators*. Only you have write access to SRCI_PY,
   because whoever can change the workflows can use the deploy key.

Until the secret exists, the job only prints a notice and succeeds.

## Workflow for SDK changes

- Change the SDK locally (CUSTOM markers, `srci_py_harness/CUSTOM_CHANGES.md`), commit, and
  `git push` to the private repository.
- The next CI run of SRCI_PY builds the new version. To pin a version, set `SDK_REF`.
- The local DLL for your own test runs is still built with `srci_py_harness\build.bat`.
