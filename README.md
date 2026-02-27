# Project Disclaimer
This project demonstrates common pitfalls and testing challenges in **Django** applications
using **Server-Side Rendering (SSR)**.

---

# Project Details
The core functionality revolves around a form where users define operating hours for their shops.
While the standard expected input is a range like `10:00 - 18:00`,
the system must flexibly handle specific edge cases and midnight transitions.

### Operating Hours Logic
| Scenario | Input Examples | System Interpretation |
| :--- | :--- | :--- |
| **Standard** | `10:00 - 18:00` | Open from morning until evening. |
| **Until Midnight** | `10:00 - 24:00` | Shop operates until the end of the day. |
| **24/7 (Non-stop)** | `00:00 - 24:00` | Shop is open all day. |


### Technical Constraints
* **Time Format:** Must follow the 24-hour format (e.g., `%H:%M` -> `13:45`).
* **Minimum Duration:** Shops must remain open for a minimum duration, subject to a **configurable global setting**.
* **Flexibility:** Both the time format and the minimum working hours should be easily adjustable in the project settings.
* **User data:** To make it easy and consistent for the user, all inputs like `24:00` should be allowed and considered to be `00:00` or `midnight`.

---

# Run it

1. Copy and rename `./docker/env-sample` to `./docker/.env`
2. Adjust ENVs in `.docker/.env` as and if needed
3. Copy and rename `./django_src/settings/settings-sample.py` to `./django_src/settings/settings.py`
4. Adjust any settings, if needed
5. Run `docker-compose up --build`

> Note: Both local `.env` and `settings.py` are excluded from git, so you are free to do whatever you like.
