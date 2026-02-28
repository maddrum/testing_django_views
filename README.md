# Project Disclaimer
This project demonstrates common pitfalls and testing challenges in **Django** applications
using **Server-Side Rendering (SSR)**. It is for demonstration purposes related to the

---

# Project Details
You are developing a mall shop operating hour platform.
The product tracks shop names and hours so customers know exactly when their favorite shops are open
and never miss a chance to buy new jeans or shoes for going too early or too late, which happens all the times!

### Core Specifications
| Feature | Requirement |
| :--- | :--- |
| **Shop Name** | Unique shop name for each business |
| **Opening Hour** | Time the shop starts operations |
| **Closing Hour** | Time the shop ends operations |

---

### Technical Constraints
| Constraint | Specification |
| :--- | :--- |
| **Time Format** | 24-hour format, %H:%M format - e.g., `08:42`, `13:45` |
| **Earliest Opening** | `07:00` |
| **Latest Closing** | `22:00` |

---

# Run it

1. Copy and rename `./docker/env-sample` to `./docker/.env`
2. Adjust ENVs in `.docker/.env` as and if needed
3. Copy and rename `./django_src/settings/settings-sample.py` to `./django_src/settings/settings.py`
4. Adjust any settings, if needed
5. Run `docker-compose up --build`

> Note: Both local `.env` and `settings.py` are excluded from git, so you are free to do whatever you like.
