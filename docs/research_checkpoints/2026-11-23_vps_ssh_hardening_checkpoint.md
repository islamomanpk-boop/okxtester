# VPS SSH Hardening Checkpoint — 2026-11-23

**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Purpose:** Record the VPS administrator-access setup and SSH hardening actions completed on 2026-11-23. This is an operations record, separate from the trading research roadmap.

## 1. Administrator access established

- Created the separate Linux account `researchadmin`.
- Set an account password locally on the VPS; the password is not recorded here.
- Added `researchadmin` to the `sudo` group.
- Created `/home/researchadmin/.ssh/authorized_keys` and installed the user's Ed25519 public key.
- Verified SSH directory/file ownership and restrictive permissions:
  - `/home/researchadmin/.ssh`: owner `researchadmin`, mode `700`.
  - `authorized_keys`: owner `researchadmin`, mode `600`.
- Compared the public-key fingerprint on Termux with the installed VPS key; fingerprints matched.
- Successfully logged in as `researchadmin` using the private key from Termux.
- Successfully ran `sudo whoami`, which returned `root`.

No private key, passphrase, account password, public IP address, or login-source IP address is recorded in this repository.

## 2. SSH configuration backup

Before changing SSH settings, a backup was created at:

```text
/root/ssh-config-backup-2026-11-23/
```

It contains copies of:
- `/etc/ssh/sshd_config`
- `/etc/ssh/sshd_config.d/`

## 3. SSH hardening configuration applied

Created:

```text
/etc/ssh/sshd_config.d/00-local-hardening.conf
```

With these settings:

```sshconfig
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
KbdInteractiveAuthentication no
AuthenticationMethods publickey
MaxAuthTries 3
```

The configuration was checked with `sshd -t` and passed. Before reload, `sshd -T` reported the intended effective values:
- `permitrootlogin no`
- `passwordauthentication no`
- `pubkeyauthentication yes`
- `kbdinteractiveauthentication no`
- `authenticationmethods publickey`
- `maxauthtries 3`

The SSH service was successfully reloaded with `systemctl reload ssh`; service status showed it remained active and the reload validation completed successfully.

## 4. Post-reload access test

After the reload, a completely new Termux session successfully established a fresh SSH connection as `researchadmin` using the Ed25519 key.

This verifies that the new key-based administrator login continued to work after the SSH configuration reload.

## 5. Remaining verification

At the time this checkpoint was written:
- Re-run `sudo sshd -t` and `sudo sshd -T` from the fresh `researchadmin` session to confirm the current effective settings.
- Re-run `sudo whoami` to confirm sudo access in that fresh session.
- Keep the working `researchadmin` session open during verification.
- Do not remove the backup or assume recovery is unnecessary.
- Do not change SSH port, firewall rules, DigitalOcean firewall settings, or other services as part of this checkpoint.

The old root session may remain connected even though new direct root SSH login is configured to be denied. Existing sessions are not proof that a new root login is permitted.

## 6. Recovery and safety notes

- Preserve the root configuration backup at the path above until access has been independently verified and a recovery plan is no longer needed.
- If a future SSH change causes access trouble, use the existing authenticated session or the VPS provider's console/recovery mechanism; do not delete lock files or make broad configuration edits.
- Never commit private keys, passphrases, passwords, API credentials, or sensitive authentication logs.

---

**Status:** SSH key-based administrator access established; SSH hardening configuration validated, reloaded, and fresh-key-login tested. Final effective-settings/sudo verification remains pending.
