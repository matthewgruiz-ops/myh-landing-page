# MYH Gateway Deployment and Rollback Notes

Author: **Manus AI**  
Date: **2026-06-04**

## Purpose

This document records how the updated **MyYachtHub public gateway** should be reviewed, deployed, and rolled back. The implementation intentionally changes only the `myh-landing-page` repository. It does **not** delete, overwrite, or merge the existing **Vessel Knowledge Platform**, **Onboard**, or **World Map** applications.

## Changed repository

| Item | Value |
|---|---|
| Repository | `matthewgruiz-ops/myh-landing-page` |
| Working branch | `safe-gateway-preserve-legacy-20260604` |
| Local path | `/home/ubuntu/myh_repo_audit/myh-landing-page` |
| Primary changed route | `/` |
| Preserved legacy route | `/legacy/` |
| New product access routes | `/onboard/`, `/world-map/`, `/ecosystem/` |

The new gateway positions **MYH** as the parent brand and provides short, polished access pages for the existing products. The previous public homepage has been copied intact to `/legacy/` before the root homepage was replaced.

## Protected application boundaries

| Protected asset | Repository | Rule |
|---|---|---|
| Current MYH legacy landing page | `matthewgruiz-ops/myh-landing-page` | Keep the preserved page available at `/legacy/` and do not delete its assets. |
| Vessel Knowledge Platform | `matthewgruiz-ops/myh-platform` | Leave `app.myyachthub.co.uk` and platform routes untouched. Do not merge Onboard or World Map into this app. |
| Onboard | `matthewgruiz-ops/myh-onboard` | Treat as an existing standalone app. The gateway only provides a public access page at `/onboard/`. |
| World Map | `matthewgruiz-ops/myh-world-map` | Treat as an existing standalone app. The gateway only provides a public access page at `/world-map/`. |

## Route plan

| Public route or target | Current behavior in this branch | Deployment note |
|---|---|---|
| `/` | New parent MYH gateway homepage. | Safe to deploy after review. |
| `/legacy/` | Preserved previous landing page. | Used as rollback-visible archive and proof that the old page was not deleted. |
| `/onboard/` | Short Onboard product/access page. | Does not link to `onboard.myyachthub.co.uk` until the standalone app is live. |
| `/world-map/` | Short World Map product/access page. | Does not link to `map.myyachthub.co.uk` until the standalone map app is live. |
| `/ecosystem/` | Demo page with **Fix**, **Plan**, and **Connect** sections. | Fix and Plan route internally to product access pages; Connect is a complete Coming Soon section. |
| `app.myyachthub.co.uk` | External protected platform link. | No platform changes were made. |

## Standalone product deployment requirements

The gateway can be reviewed and deployed independently from the standalone products. The product app domains should only be enabled after each application has its own hosting, database, secrets, and authentication configuration in place.

| Product | Intended standalone domain | Required before enabling direct public CTAs |
|---|---|---|
| Onboard | `onboard.myyachthub.co.uk` | Deploy the existing `myh-onboard` app with its database, OAuth/session configuration, owner identity settings, and storage-related variables. |
| World Map | `map.myyachthub.co.uk` | Deploy the existing `myh-world-map` app with its database, JWT secret, admin email list, and optional notification/storage variables. |

Until those deployments are confirmed live, this branch deliberately keeps product CTAs on internal access anchors and email request links. This avoids sending visitors to unavailable subdomains while preserving the final domain architecture.

## Validation performed

The static validation script was run from the landing-page repository:

```bash
python3 validate_gateway.py
```

The validation passed and checked the expected static routes, link integrity, required assets, and the preserved legacy checksum. Local browser review was also completed for `/`, `/legacy/`, `/onboard/`, `/world-map/`, and `/ecosystem/` using a local static server.

## Review command

To review locally from the repository root:

```bash
python3 -m http.server 4173
```

Then open:

```text
http://127.0.0.1:4173/
http://127.0.0.1:4173/legacy/
http://127.0.0.1:4173/onboard/
http://127.0.0.1:4173/world-map/
http://127.0.0.1:4173/ecosystem/
```

## Rollback path

If the new gateway should not go live, the safest rollback is to keep the branch unmerged and leave the current production branch untouched. If the branch is merged and then needs to be reverted, restore the previous root `index.html` from `/legacy/index.html` or revert the merge commit in Git.

The preserved route means the old homepage remains available in the deployed artifact even after the new gateway homepage is introduced. This is not a substitute for Git rollback, but it provides an additional content-level safety net.

## Production recommendation

The recommended next step is to review the branch visually and confirm the copy and CTA behavior. Only after approval should the branch be pushed or merged for deployment. The standalone Onboard and World Map applications should be deployed separately on their own subdomains before the gateway CTAs are changed to point directly at those app domains.
