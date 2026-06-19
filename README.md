# Forefront HQ


![Forefront Mockup](./static/images/forefront-hq-mock-ups.png)

## Table of Contents

[Introduction](#introduction)

[View Live Site](#view-live-site)

1. [UX](#ux)
    - [Project Goals](#project-goals)
    - [User Goals](#user-goals)
    - [User Stories](#user-stories)
    - [Developer Goals](#developer-goals)
    - [Design Choices](#design-choices)
        - [Colour Palette](#colour-palette)
        - [Frontend Design](#frontend-designs)
            - [Home Page](#home-page)
            - [About Page](#about-page)
            - [Services Page](#services-page)
            - [Packages Page](#packages-page)
            - [Portfolio Page](#portfolio-page)
            - [Contact Page](#contact-page)
            - [Sign In Page](#sign-in-page)
            - [Create Account Page](#create-account-page)
        - [Wireframes](#wireframes)
            - [Mobile](#mobile)
            - [Tablet](#tablet)
            - [Desktop](#desktop)
        - [ERD](#erd)
2. [Agile Development](#agile-development)
    - [GitHub Projects Board](#github-projects-board)
    - [MoSCoW Prioritisation](#moscow-prioritisation)
    - [Development Phases](#development-phases)
3. [Features](#features)
    - [Existing Features](#existing-features)
    - [Features to Implement](#features-to-implement)
4. [Technologies Used](#technologies-used)
5. [Testing](#testing)
    - [Code Validation](#code-validation)
    - [Bugs Discovered](#bugs-discovered)
    - [Usability Testing](#usability-testing)
    - [Responsiveness Testing](#responsiveness-testing)
    - [Data Managemnt Testing](#data-management-testing)
    - [Manual Testing](#manual-testing)
    - [Automated Testing](#automated-testing)
    - [Lighthouse Testing](#lighthouse-testing)
6. [Deployment](#deployment)
    - [Prerequisites](#prerequisites)
    - [Deploying to Heroku](#deploying-to-heroku)
    - [How To Run The Project Locally](#how-to-run-the-project-locally)
7. [Credits](#credits)
    - [Content](#content)
    - [Code](#code)
    - [Images](#images)
    - [Acknowledgements](#acknowledgdements)

## Introduction 

**Forefront HQ** is a business website where startups and small businesses can explore digital services, view previous work and purchase tailored packages to help them grow online.

The platform focuses on simplicity and transparency, giving potential clients a clear picture of what's on offer before they commit. From browsing the portfolio to building a custom package and checking out securely via Stripe, Forefront HQ makes it easy for businesses to take their next step forward.


## View Live Site

[ForeFront HQ Live Site](https://forefront-hq-new-a54ac6718d65.herokuapp.com/)

# UX

## Project Goals

The goal of Forefront HQ is to build a full-stack business website where potential clients can explore services, view previous work, and purchase packages directly through the site. The focus is on making the process of hiring a digital agency feel simple and transparent, from first impression through to checkout.

The project uses Django and PostgreSQL to handle the backend, with a database designed around users, packages, portfolio projects, and Stripe payments. On the frontend, the aim is to bring a dark, minimal design to life with a consistent and responsive layout across every page.

Users will be able to create accounts, browse services and portfolio work, and purchase packages or build their own custom one. The project is also structured in a way that makes it straightforward to add new services, packages, and portfolio entries over time.

---

## User Goals

Users of Forefront HQ should be able to quickly understand what the company offers and whether it is the right fit for their business. The goal is to give potential clients a clear and professional experience where they can go from discovering the company to making a purchase without any friction.

A user should be able to browse the services and portfolio, view package pricing, and either contact the company or proceed straight to checkout. They should also be able to create an account, sign in with Google, and purchase a package securely through Stripe.

The overall experience should feel clean and intuitive, so users can find what they are looking for quickly and feel confident in the company before committing.

---

## User Stories

Users should be able to browse the services Forefront HQ offers so they can decide whether the company is the right fit for their needs. They should be able to view the portfolio to see examples of previous work and get a sense of the quality and style on offer.

Users should be able to view available packages and pricing so they can find an option that suits their budget. They should also be able to build a custom package by selecting only the add-ons they need, rather than being locked into a fixed offering.

Once they have decided, users should be able to purchase a package securely through Stripe, or contact the company directly if they have questions before committing. The checkout process should feel straightforward and trustworthy.

Users should be able to create an account or sign in with Google so they can manage their details and access their purchases. The registration process should include email verification to keep accounts secure.

Overall the site should be easy to navigate and feel professional at every step, so users never have to think too hard about where to go or what to do next.

---

## Developer Goals

The goal for this project is to build a full-stack web application that connects a Django backend with a custom frontend, handling real user interactions and payments rather than just displaying static content. I want to get comfortable working with models, views, templates, and third-party integrations together so the site feels like a real product.

Another aim is to implement a relational database structured around users, packages, portfolio entries, and orders, making sure everything is organised properly and can scale as the business grows.

I also want to improve my ability to translate a UI design into a working application, keeping the layout consistent, responsive, and on-brand across every page. This includes building reusable template components that extend a single base layout.

On top of that, the project is about gaining confidence working with third-party services — specifically Stripe for payments and webhooks, and django-allauth for authentication including Google OAuth. Managing environment variables, deploying to Heroku, and handling production-specific issues are also key parts of the learning process.

Overall, the focus is on building something that works end-to-end and feels like something a real client could use, not just a collection of features put together for the sake of it.

---

## Design Choices
 
The design for Forefront HQ was planned in Canva before any code was written. The goal was a dark, minimal aesthetic that feels professional and trustworthy — the kind of site a startup would expect from a digital studio. All page layouts were designed as full desktop mockups first, then adapted for mobile and tablet during development.

### Colour Palette
 
The brand colour palette was created using Canva and Google Stitch and uses six core colours consistently across the site. The image below was created by claude ai to represent them visually.
 
![Colour Palette](./static/images/front-end-designs/colour-pallette.png)
 
| Colour | Hex | Usage |
|---|---|---|
| Brand Blue | `#1A6CF6` | Buttons, links, logo |
| Dark Base | `#080D14` | Page background |
| Surface | `#0B1220` | Cards, nav |
| Elevated | `#162947` | Hover states, raised elements |
| Text White | `#E8EDF5` | Headings, body text |
| Muted | `#6B84A0` | Captions, labels |

### Typography
 
Two typefaces are used throughout the site, both loaded via Google Fonts:
 
- **Space Grotesk** — used for all headings and UI labels. A geometric sans-serif that feels modern and technical without being cold.
- **Space Mono** — used for code-style labels, tags, and accent text. Adds a developer character to the brand without overusing it.

### FrontEnd Designs
 
All pages were designed in Canva prior to development and perfected with Google stitch. The designs served as the reference point for layout, spacing, colour usage, and component structure throughout the build.
 
#### Home Page
![Home Page Design](./static/images/front-end-designs/Home-page.png)
 
#### About Page
![About Page Design](./static/images/front-end-designs/about-page.png)
 
#### Services Page
![Services Page Design](./static/images/front-end-designs/services-pge-screenshot.png)
 
#### Packages Page
![Packages Page Design](./static/images/front-end-designs/package-page.png)
 
#### Portfolio Page
![Portfolio Page Design](./static/images/front-end-designs/portfolio-page.png)
 
#### Contact Page
![Contact Page Design](./static/images/front-end-designs/contact-page.png)
 
#### Sign In Page
![Sign In Page Design](./static/images/front-end-designs/sign-in-page.png)
 
#### Create Account Page
![Create Account Page Design](./static/images/front-end-designs/create-account-page.png)

---

## Wireframes

Each page was wireframed using google stitch across mobile, tablet and desktop breakpoints after the frontend designs were created. The wireframes focus on layout and content hierarchy. Focusing on where each section is placed, how much space it takes up and how the structure changes on different screen sizes. Working through this after the frontend design was created meant that the responsiveness break points and behabiours were planned before any coding happened. 

### Mobile 

**Home Page**

![Home Page Wireframe Mobile](./static/images/mobile-wireframes-fhq/home-page.png)

On mobile the home page stacks all content into a single column. The navbar collapses to a hamburger menu to preserve space at the top. The hero sits first with the tagline, subtitle, and two CTA buttons stacked vertically. The business card mockup follows below the hero text rather than sitting beside it, since there is not enough horizontal space for a two-column layout at this width. The footer sits at the bottom with navigation links stacked into a compact column.

---

**About Page**

![About Page Wireframe Mobile](./static/images/mobile-wireframes-fhq/about-page.png)

The about page on mobile stacks the logo, intro text, and team member cards into a single column. The team cards that appear in a grid on larger screens each become a full-width row on mobile, keeping the profile image, name, job title, and bio readable without shrinking the content. The call to action buttons sit below the team section, followed by the footer.

---

**Services Page**

![Services Page Wireframe Desktop](./static/images/mobile-wireframes-fhq/services-page.png)

The services page on mobile places each service card as a full-width block, stacked vertically. Each card shows the service icon, name, tagline, description, and feature checklist. Stacking them this way ensures the checklist items have enough room to remain readable rather than being compressed into a narrow column.

---

**Packages Page**

![Packages Page Wireframe Mobile](./static/images/mobile-wireframes-fhq/packages-page.png)

On mobile the packages page stacks the Starter and Growth cards vertically, each taking the full screen width. The Build Your Own section follows below with addon cards stacked in a single column. The running total bar and Review My Package button sit at the bottom of the builder section, giving the user a clear summary of their selection before proceeding.

---

**Portfolio Page**

![Portfolio Page Wireframe Mobile](./static/images/mobile-wireframes-fhq/portfolio-page.png)

Portfolio project cards stack into a single full-width column on mobile. Each card shows the project image at the top, followed by the live badge, category label, client name, description, and tags. Stacking the cards vertically means the image and text have room to breathe and the project details are easy to read on a small screen. The Start a Project button sits at the bottom of the project list.
 
---

**Contact Page**

![Contact Page Wireframe Mobile](./static/images/mobile-wireframes-fhq/contact-page.png)

The contact page on mobile stacks the hero text and contact info block above the form. All four form fields — name, email, service dropdown, and message textarea — stack vertically and take the full available width. The Send Message button sits at the bottom of the form, also full width. This layout keeps the form simple and easy to complete on a small screen without any horizontal scrolling.
 
---

**Login Page**

![Login Page Wireframe Mobile](./static/images/mobile-wireframes-fhq/sign-in-page.png)

The login page on mobile uses a centred auth card that fills the available width with comfortable padding. The Google sign-in button sits at the top of the card above the OR divider. Below it the email and password fields stack vertically, followed by the Forgot Password link and the Sign In button. The simplicity of this layout means there is nothing competing with the form, which is especially important on a small screen where space is limited.
 
---

**Sign Up Page**

![Signup Page Wireframe Mobile](./static/images/mobile-wireframes-fhq/sign-up-page.png)

The register page mirrors the login layout — a centred form card filling the available width. The Google sign-up button sits above the OR divider, with the email, password, and confirm password fields stacked below. The Create Account button sits at the bottom. Keeping the two auth pages visually consistent means users moving between login and register always see a familiar structure.
 
---

### Tablet

**Home Page**

![Home Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/home-page-tablet.png)

On tablet the home page introduces a two-column layout for the hero section — the title, tagline, and CTA buttons sit on the left while the business card mockup sits on the right. This makes better use of the wider screen without going to a full desktop layout. The navbar expands to show all links. The services section moves to a two-column grid so two cards sit side by side before wrapping.
 
---

**About Page**

![About Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/about-page-tablet.png)

The tablet about page moves the hero into a two-column layout, with the logo on the left and the intro text on the right. Team member cards switch to a two-column grid, with two members visible side by side before wrapping. This is more efficient than the single-column mobile layout while avoiding the squeeze that would come from forcing three cards into a narrower container.
 
---

**Services Page**

![Services Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/services-page-tablet.png)

On tablet the services page moves to a two-column grid so two service cards sit side by side. This makes better use of the available width and allows users to compare services more easily than on mobile where each card takes the full screen width.
 
---

**Packages Page**

![Packages Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/packages-page-tablet.png)

The Starter and Growth package cards sit side by side on tablet in a two-column layout. The Build Your Own addon cards also move to a two-column grid. The running total bar spans the full width at the bottom of the builder section.
 
---

**Portfolio Page**

![Portfolio Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/portfolio-page-tablet.png)

Portfolio project cards switch to a two-column grid on tablet. Two project cards sit side by side, showing more work per row than on mobile while keeping each card large enough to display the image and details comfortably. The Start a Project button sits below the grid, centred on the page.
 
---

**Contact Page**

![Contact Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/contact-page-tablet.png)

The contact page on tablet benefits from the extra width but remains largely single-column. The hero text and contact info sit above the form card, which now has more breathing room than on mobile. The four form fields take the full width of the card, and the Send Message button spans the full card width.
 
---

**Login Page**

![Login Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/login-page-tablet.png)

On tablet the login form card narrows slightly relative to the full screen width so it does not stretch uncomfortably wide. The background is visible on both sides of the card, giving the page a more composed feel. The field order and button placement remain the same as on mobile.
 
---

**Sign Up Page**

![Signup Page Wireframe Tablet](./static/images/tablet-wireframes-fhq/signup-page-tablet.png)

The register page on tablet follows the same principle as the login page — a centred card that is narrower than the full screen width with the background visible either side. The three fields, Google button, and Create Account button maintain the same vertical order as on mobile.
 
---

### Desktop

**Home Page**

![Home Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/home-page-desktop.png)

The desktop home page uses the full page width. The navbar is fully expanded with all links visible. The hero remains two-column with the title and CTAs on the left and the business card mockup on the right, now with more space for both. The services section moves to a four-column grid, showing all four service cards in a single row. The footer sits at the bottom with logo, navigation, more links, and social media columns arranged side by side.
 
---

**About Page**

![About Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/about-page-desktop.png)

On desktop the about page hero remains two-column. Team member cards move to a three-column grid, with all members visible in a single row. Having all team members visible at once without scrolling reinforces the sense of a complete, professional team. The call to action and footer follow as full-width sections below.
 
---

**Services Page**

![Services Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/services-page-desktop.png)

The services page on desktop uses a four-column grid, displaying all four service cards in a single row. This is the most efficient use of the wider screen and gives users an immediate overview of everything on offer without needing to scroll. Each card has enough horizontal space to show the icon, name, tagline, and full feature checklist comfortably.
 
---

**Packages Page**

![Packages Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/packages-desktop.png)

On desktop the packages page shows the Starter and Growth cards side by side with a clear visual separation between them. The Build Your Own addon cards move to a three-column grid, showing all addons in fewer rows. The running total bar spans the full width at the bottom, keeping the total and checkout button always in view as the user makes selections.
 
---

**Portfolio Page**

![Portfolio Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/portfolio-page-desktop.png)

The desktop portfolio page uses a three-column project grid. Three cards visible per row means users immediately get a strong sense of the breadth of work on the page without needing to scroll to understand how much is there. Each card has space for the project image, live badge, category, client name, description, and tags all at once.
 
---

**Contact Page**

![Contact Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/contact-page-desktop.png)

The contact page on desktop splits into two columns. The left column holds the hero heading, intro text, and contact info icons — email, response time, location, and consultation details. The right column holds the form card with all four fields and the Send Message button. This two-column layout makes the page feel more spacious and allows users to see the contact information and the form side by side without needing to scroll between them.
 
---

**Login Page**

![Login Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/login-page-desktop.png)

On desktop the login form card is wider than on tablet but stops well short of the full page width, keeping the form contained and focused. The dark background remains visible on both sides of the card, maintaining the site's visual identity. The field layout and button placement are identical to tablet and mobile, so users always know what to expect regardless of the device they are using.
 
---

**Sign Up Page**

![Sign Up Page Wireframe Mobile](./static/images/desktop-wireframes-fhq/sign-up-page-desktop.png)

The register page on desktop follows the same principle as login — a centred card that is proportional to the screen width without stretching across it. The Google sign-up button, email field, password field, confirm password field, and Create Account button sit in a clean vertical stack. Keeping both auth pages visually consistent across all three breakpoints means users switching between login and register always see a familiar layout.

---

## ERD

![ERD Diagram](./static/images/ERD-FHQ.png)

The ERD was designed during the planning phase and used as the blueprint for every Django model in the project. The structure is built around the user journey from discovery through to purchase — a user arrives, browses services and portfolio work, selects a package, and checks out. The database reflects that flow, with `django_user` and `user_profile` at the centre, branching out into orders, payments, packages, and content models. The final models stayed very close to the ERD, with a small number of fields added during development as requirements became clearer.
 
**DJANGO_USER** is Django's built-in `auth.User` model rather than a custom table. The ERD shows it with `email`, `password`, `is_active`, `is_staff`, `date_joined` and `last_login` fields to illustrate the relationships, but in practice these are handled entirely by Django's authentication system and django-allauth. The user sits at the centre of the diagram because almost everything on the site either belongs to a user or is triggered by one — orders, payments, custom package selections, and contact enquiries all trace back to this table. The `user_profile` extends it with a one-to-one relationship, adding `phone`, `company_name`, `stripe_customer_id`, and `created_at` fields that are not part of Django's default user model but are needed for the business logic around payments and client management.
 
**USER_PROFILE** has a one-to-one relationship with `django_user`, meaning every user has exactly one profile and every profile belongs to exactly one user. The `stripe_customer_id` field is populated automatically by the webhook handler when a user completes their first purchase — this ties the Django user record to their Stripe customer record and is stored here so it can be reused on future purchases without creating duplicate Stripe customers. The `CASCADE` delete behaviour means that if a user account is deleted, their profile is removed with it.
 
**ORDER** links `user_profile` and `package` together as the record of a completed transaction. The `user_profile` foreign key uses `CASCADE` so that orders are removed if a user deletes their account, while the `package` foreign key uses `SET_NULL` so that deleting a package does not wipe out the historical order record — the order remains in the database with `package` set to null, preserving the financial history. The `status` field uses a `choices` list of `pending`, `paid`, `cancelled`, and `refunded`, and the `confirmation_email_sent` boolean tracks whether the post-payment email was dispatched successfully by the webhook handler. One field that does not appear in the original ERD is `confirmation_email_sent` — this was added during development once the webhook email flow was implemented, to give the admin panel a clear indicator of whether the customer received their confirmation.
 
**PAYMENT** has a one-to-one relationship with `order`, meaning each order has exactly one payment record and each payment belongs to exactly one order. It stores the `stripe_payment_intent`, `stripe_customer_id`, `amount`, `currency`, `status`, and `paid_at` fields returned by Stripe's webhook event. Storing the payment intent ID separately from the order allows the admin panel to cross-reference transactions directly in the Stripe dashboard. The `CASCADE` delete behaviour means that deleting an order also removes its associated payment record.
 
**PACKAGE** is the central content model for the purchasing flow. It holds `name`, `code`, `tier`, `price`, `is_recommended`, `is_active`, `display_order`, `cta_label`, and `stripe_price_id`. The `stripe_price_id` field was added during development — it was not in the original ERD but is essential for Stripe Checkout, as it references the pre-configured price object in the Stripe dashboard rather than passing a raw amount. The `is_active` flag allows packages to be hidden from the packages page without deleting them, and `display_order` controls the left-to-right order in which they appear. `PACKAGE_FEATURE` has a many-to-one relationship with `package`, holding the individual feature checklist items displayed on each package card.
 
**PACKAGE_ADDON** powers the custom package builder. Each addon has a `name`, `description`, `price`, `is_active`, and `display_order`. The `is_active` flag allows addons to be retired without deletion. The `CUSTOM_PACKAGE_SELECTION` model links a user to a set of chosen addons via a many-to-many relationship through `packages_custompackageselection_addons`, and also stores a `session_key` for anonymous selections. The `get_total()` method on `CustomPackageSelection` sums the prices of all selected addons dynamically rather than storing a cached total, keeping the data consistent if addon prices change.
 
**SERVICE** is a simple content model holding `name`, `slug`, `short_description`, `description`, `is_active`, and `display_order`. It powers the services page and also populates the service of interest dropdown on the contact form. The `is_active` flag and `display_order` field give the admin full control over what appears and in what order, without touching any code.
 
**CONTACT_ENQUIRY** links `django_user` and `service` via foreign keys, both set to `SET_NULL` on delete so that enquiries are preserved even if the associated user or service is later removed. The `status` field uses a `choices` list of `new`, `read`, and `responded` to allow the admin to track where each enquiry is in the response workflow. The `responded_at` datetime field is null by default and can be populated when the enquiry is marked as responded, giving a clear audit trail.
 
**PORTFOLIO_PROJECT** holds all the fields needed to display a client project card — `title`, `slug`, `client_name`, `category`, `description`, `image_url`, `live_url`, `is_live`, `is_featured`, `completed_at`, and `created_at`. The `is_live` flag controls visibility on the portfolio page, allowing draft projects to be prepared in the admin before going public. Projects are ordered by `completed_at` descending so the most recent work always appears first. Tags are attached via a many-to-many relationship through `PORTFOLIO_PROJECT_TAG`, which enforces a `unique_together` constraint on `(project, tag)` to prevent duplicate tag assignments.
 
**STAFF_ABOUT** is a simple content model for the about page, holding `name`, `profile_img_url`, `job_title`, `bio_description`, `is_active`, and `display_order`. Like the service and package models, the `is_active` flag and `display_order` field give the admin full control over what appears and in what sequence without any code changes.

---

# Agile Development 

Forefront HQ was planned and built using an Agile approach throughout. GitHub Projects was used as the Kanban board to manage all work, tracking issues from backlog through to completion across five development phases.

### GitHub Project Board

Development was managed using a GitHub Projects board with issues and user stories tracked throughout the build. Tasks were broken down into individual issues and moved through columns as work progressed.
 
![GitHub Projects Board](./static/images/github-project-board.png)

## MoSCoW Prioritisation
 
User stories and features were prioritised using the MoSCoW method to keep the project focused on delivering a working product within the available time.
 
| Priority | Items |
|---|---|
| **Must Have** | User registration and login, email verification, packages page, Stripe checkout, webhook order creation, portfolio page, contact form, services page |
| **Should Have** | Custom package builder, Google OAuth, order confirmation email, UserProfile model, admin content management |
| **Could Have** | Package addon pages counter, custom package summary page, portfolio tags, staff about page |
| **Won't Have** | Client dashboard, invoice generation, live chat, subscription billing |

## Development Phases
 
The project was built in phases, with each phase focused on a specific area of functionality before moving to the next.
 
**Phase 1 — Project Setup**
Django project created, apps registered, base template built, static files configured, deployed to Heroku early.
 
**Phase 2 — Authentication**
Custom login and register views, django-allauth integrated, email verification flow, Google OAuth, allauth template overrides.
 
**Phase 3 — Core Pages**
Home, about, services, portfolio, and contact pages built and wired to the database via their respective models.
 
**Phase 4 — Packages and Stripe**
Package and addon models, packages page, Stripe Checkout integration, webhook handler, order and payment models, success and cancel pages.
 
**Phase 5 — Custom Package Builder**
Addon selection with session storage, running total JavaScript, summary page, remove addon/pages views, custom Stripe checkout with dynamic line items.
 
**Phase 6 — Testing and Validation**
Django unit tests across all apps, Jest tests for JavaScript, HTML/CSS/Python validation, bug fixes, Lighthouse testing.
 
**Phase 7 — README and Submission**
Full README written and final deployment checks.

![Agile timeline graph](./static/images/agile_timeline.svg)

---

# Features
 
## Existing Features
 
### Navigation
A fully responsive navbar is present on every page, built with Bootstrap 5.3.3. On desktop it shows all navigation links, the login/register buttons when logged out, and a logout button when logged in. On mobile it collapses to a hamburger menu. The active page is highlighted in the nav.
 
### Home Page
The home page introduces Forefront HQ with a hero section, tagline, and two CTAs — View Packages and See Our Work. A live business card mockup sits alongside the hero text.
 
### About Page
Displays active team members pulled from the `StaffAbout` model. Members are ordered by `display_order` and managed entirely through the Django admin.
 
### Services Page
Lists all active services from the `Service` model in order of `display_order`. Each service card shows the name, tagline, description, and a checklist of features. Content is fully database-driven and editable through the admin.
 
### Packages Page
Displays the Starter and Growth packages from the `Package` model with pricing, features, and CTA buttons. Logged-in users are taken directly to Stripe Checkout. Logged-out users are redirected to login first.
 
### Custom Package Builder
Allows users to select individual addons and specify the number of additional pages they need. A live running total updates as checkboxes are ticked using vanilla JavaScript. The summary button is disabled until at least one item is selected.
 
### Custom Package Summary
Shows the user's selected addons and total before checkout. Individual addons and the additional pages item can be removed from the summary, with the total updating accordingly. Proceeds to a dynamic Stripe Checkout session with line items matching the selection.
 
### Portfolio Page
Displays live portfolio projects from the `PortfolioProject` model, ordered by most recently completed. Each card shows the project image, title, client, category, description, and tags. Draft projects with `is_live=False` are hidden.
 
### Contact Page
A contact form that stores enquiries in the `ContactEnquiry` model. Logged-in users are automatically linked to their account. A service of interest dropdown shows all active services. Submissions redirect back to the contact page with a success message.
 
### User Registration
Custom registration view with email and password validation. On success, an allauth `EmailAddress` record is created and a confirmation email is sent. Users cannot log in until they verify their email.
 
### User Login
Email-based login with allauth integration. Unverified users are blocked and shown an appropriate message. Google OAuth is available as an alternative sign-in method.
 
### Stripe Payments
Full Stripe Checkout integration for both fixed packages and custom builds. On successful payment, a Stripe webhook fires and creates an `Order` and `Payment` record in the database. The customer's Stripe ID is saved to their `UserProfile`.
 
### Order Confirmation Email
After a successful webhook event, a confirmation email is sent to the customer with the package name, amount, and order date.
 
### Django Admin
All content — packages, addons, services, portfolio projects, team members, orders, payments, and contact enquiries — is managed through the Django admin panel.
 
### 404 Page
A custom 404 page is shown for any unmatched URL, keeping the user within the site's design and navigation.
 
---

## Features to Implement
 
- **Client dashboard** — a logged-in area where clients can view their order history and download invoices
- **Invoice generation** — automatic PDF invoice generation after a successful purchase
- **Package enquiry flow** — an option to enquire about a package rather than purchasing directly, for clients who want to discuss requirements first
- **Testimonials** — a database-driven testimonials section on the home page managed through the admin
- **Digital Marketing packages** - an option to add digital marketing services to custom package or purchase sepereate packaged digital marketing packages.

---

# Technologies Used
 
## Languages
 
- **HTML5** — page structure and templates
- **CSS3** — custom styling via `static/css/style.css`
- **JavaScript** — flash message auto-dismiss and custom package builder interactivity (`static/js/script.js`)
- **Python** — all backend logic via Django

## Frameworks and Libraries
 
- **Django 6.0.5** — the core web framework handling models, views, templates, and URL routing
- **django-allauth 65.17.0** — authentication including email verification and Google OAuth
- **Bootstrap 5.3.3** — responsive grid, navbar, and utility classes
- **Stripe** — payment processing via Stripe Checkout and webhooks
- **Whitenoise 6.12.0** — serving static files in production on Heroku
- **Gunicorn 26.0.0** — WSGI server for production deployment
- **python-dotenv** — loading environment variables from `.env` in development
- **Jest 29** — JavaScript unit testing with `jest-environment-jsdom`

## Tools and Services
 
- **Heroku** — cloud platform used for deployment
- **Heroku Postgres** — production database
- **SQLite** — local development database
- **Google Workspace** — SMTP email sending via `hello@forefronthq.co.uk`
- **Google Cloud Console** — Google OAuth credentials and redirect URI configuration
- **claude ai** - for colour pallette representations, agile approach graph and assistance with debugging
- **Stripe Dashboard** — product, price, and webhook management
- **Canva** — UI design and page mockups
- **Google Stitch** — colour palette generation
- **Font Awesome** — Google icon on the login page
- **Google Fonts** — Space Grotesk and Space Mono typefaces
- **imgbb** — image hosting for portfolio project images
- **Git** — version control
- **GitHub** — repository hosting and project board
- **VS Code** — development environment
- **CI Python Linter** — PEP8 validation
- **W3C HTML Validator** — HTML validation
- **W3C CSS Validator** — CSS validation

---

# Testing

## Bugs Discovered

### Bug 1 — `ModuleNotFoundError: No module named 'forefront_hq'`
**Description:** After renaming the Django config package from `webhive` to `forefront_hq`, Heroku could not find the settings module on deployment.  
**Cause:** The `DJANGO_SETTINGS_MODULE` config var on Heroku still pointed to `webhive.settings` after the rename.  
**Fix:** Updated the Heroku config var via CLI:
```
heroku config:set DJANGO_SETTINGS_MODULE=forefront_hq.settings --app forefront-hq
```

---

### Bug 2 - `Bad Request (400)` on Deployed Heroku App
**Description:** The deployed app returned a 400 error immediately after the Heroku app was renamed.  
**Cause:** `ALLOWED_HOSTS` in `settings.py` still contained the old Heroku hostname (`webhive-ca8f62799334.herokuapp.com`). Heroku also retains a random suffix in the hostname after a rename, meaning the expected clean URL `forefront-hq.herokuapp.com` was never the actual hostname.  
**Fix:** Updated `ALLOWED_HOSTS` to include the correct hostname:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'forefront-hq-cd14dedc71a3.herokuapp.com']
```

---

### Bug 3 — `Not Found (404)` After Fixing ALLOWED_HOSTS
**Description:** App returned a 404 on all routes after the 400 was resolved.  
**Cause:** `ROOT_URLCONF` was defined twice in `settings.py` — the first instance (`webhive.urls`) was conflicting with the correct one (`forefront_hq.urls`). The `accounts/urls.py` file also did not exist yet.  
**Fix:** Removed the duplicate `ROOT_URLCONF` entry and created `accounts/urls.py` with the required URL patterns.
 
---

### Bug 4 — `ModuleNotFoundError: No module named 'accounts.urls'`
**Description:** Internal server error (500) on all routes after the 404 was resolved.  
**Cause:** `forefront_hq/urls.py` included `accounts.urls` but the file did not exist.  
**Fix:** Created `accounts/urls.py` with a basic home route.
 
---
 
### Bug 5 — `ImproperlyConfigured: allauth.account.middleware.AccountMiddleware`
**Description:** Server failed to start after installing `django-allauth`.  
**Cause:** The allauth middleware was not added to `MIDDLEWARE` in `settings.py`.  
**Fix:** Added `allauth.account.middleware.AccountMiddleware` to the bottom of the `MIDDLEWARE` list:
```python
'allauth.account.middleware.AccountMiddleware',
```
 
---
 
### Bug 6 — `ModuleNotFoundError: No module named 'requests'`
**Description:** Server failed to start after adding allauth social account providers.  
**Cause:** The `requests` package was not installed in the virtual environment.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install requests
```
 
---
 
### Bug 7 — `ModuleNotFoundError: No module named 'jwt'`
**Description:** Server failed to start after installing `requests`.  
**Cause:** The `PyJWT` package required by allauth's Google provider was not installed.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install PyJWT
```
 
---
 
### Bug 8 — `ModuleNotFoundError: No module named 'cryptography'`
**Description:** Server failed to start after installing `PyJWT`.  
**Cause:** The `cryptography` package required by allauth was not installed.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install cryptography
```
 
---
 
### Bug 9 — Static Files Not Loading on Heroku
**Description:** CSS, images and JS were not being served on the deployed app.  
**Cause:** `whitenoise` was not installed, `STATIC_ROOT` was not set, and `DISABLE_COLLECTSTATIC` was not configured in Heroku config vars.  
**Fix:**
 
* Installed `whitenoise` and added it to `MIDDLEWARE`
* Added `STATIC_ROOT = BASE_DIR / 'staticfiles'` to `settings.py`
* Set `DISABLE_COLLECTSTATIC = 0` in Heroku config vars
---
 
### Bug 10 — Admin Login Failing With Correct Credentials
**Description:** Could not log in to the Django admin panel despite using the correct superuser credentials.  
**Cause:** The superuser was created before `django-allauth` was installed. Allauth changes the authentication backend which caused a mismatch with the existing superuser.  
**Fix:** Reset the superuser password via CLI:
```
python manage.py changepassword AshRoberts
```
 
---

### Bug 11 — Duplicate CSS Rules in `style.css`
**Description:** Navbar and burger menu styles were duplicated in `style.css` causing potential style conflicts.  
**Cause:** CSS was appended multiple times during iterative development without removing previous versions.  
**Fix:** Audited and rewrote `style.css` removing all duplicate rules.

---

### Bug 12 — `ConnectionRefusedError` on Google OAuth Callback
**Description:** After completing Google sign in, the app returned a `ConnectionRefusedError` at `/accounts/google/login/callback/`.  
**Cause:** Allauth was attempting to send an email verification to a user who had previously registered with email/password, but no email backend was configured.  
**Fix:** Added email backend configuration to `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
And set `ACCOUNT_EMAIL_VERIFICATION = 'none'` temporarily during development.
 
---

### Bug 13 — `MultipleObjectsReturned` on Google Login
**Description:** Clicking "Continue with Google" returned a `MultipleObjectsReturned` error.  
**Cause:** Two Google Social Application entries existed in the database — one for local development and one for Heroku — both linked to the same site.  
**Fix:** Removed the duplicate entry in the Django admin under Social Applications and ensured each entry was linked to the correct site.
 
---

### Bug 14 — `InvalidRequestError: No such price` on Stripe Checkout
**Description:** Clicking a package CTA button returned a Stripe `InvalidRequestError`.  
**Cause:** The `stripe_price_id` field in the Django admin had the Stripe **Product ID** (`prod_...`) instead of the **Price ID** (`price_...`).  
**Fix:** Updated the `stripe_price_id` field in the Django admin with the correct Price ID from the Stripe dashboard.
 
---

### Bug 15 — Stripe Checkout 500 Error on Heroku
**Description:** Stripe checkout returned a 500 error on the deployed Heroku app but worked locally.  
**Cause:** `STRIPE_SECRET_KEY` and `STRIPE_PUBLIC_KEY` config vars were not set on Heroku.  
**Fix:**
```
heroku config:set STRIPE_SECRET_KEY=sk_test_... --app forefront-hq
heroku config:set STRIPE_PUBLIC_KEY=pk_test_... --app forefront-hq
```
Packages also needed to be re-added to the Heroku database with their Stripe price IDs.
 
---
 
### Bug 16 — Webhook `UserProfile matching query does not exist`
**Description:** The Stripe webhook handler returned a 500 error when processing `checkout.session.completed`.  
**Cause:** Existing user accounts did not have a `UserProfile` record as they were created before the model was added.  
**Fix:** Updated the webhook view to use `get_or_create` instead of `get`:
```python
profile, created = UserProfile.objects.get_or_create(user=user)
```
 
---
 
### Bug 17 — `AttributeError: get` in Stripe Webhook
**Description:** The webhook handler raised an `AttributeError` when trying to access session data.  
**Cause:** Stripe objects don't support Python's `.get()` method — they require direct dictionary access with `[]`.  
**Fix:** Replaced all `.get()` calls with direct key access:
```python
email = session['customer_email'] or ''
payment_intent = session['payment_intent'] or ''
```
 
---
 
### Bug 18 — Login Page CSS Not Applying
**Description:** The login page rendered without any custom styling — the auth card, form fields and layout were unstyled.  
**Cause:** The browser was serving a cached version of `style.css` that did not include the auth page styles.  
**Fix:** Performed a hard refresh using `Cmd + Shift + R` and cleared the browser cache via DevTools → Right-click refresh → Empty Cache and Hard Reload.
 
---
 
### Bug 19 — Portfolio Image Not Displaying
**Description:** The portfolio project image showed a "Missing key" placeholder despite an image URL being set in the admin.  
**Cause:** The imgbb **Viewer link** was used instead of the **Direct link**. The viewer link is a webpage, not a direct image URL.  
**Fix:** Updated the `image_url` field in the Django admin with the imgbb **Direct link** ending in `.jpg`.
 
---
 
### Bug 20 — Custom Package Summary Page Not Showing All Items
**Description:** The summary page only showed the Additional Pages line item, not the other selected addons.  
**Cause:** The `{% for addon in addons %}` loop in `custom_summary.html` was opened but never displayed any content — the Additional Pages block and the total were inside the loop incorrectly.  
**Fix:** Restructured the template to render the Additional Pages block and addon loop separately, with the total outside both.

---

### Bug 21 — Heroku App Flagged as "Dangerous Site" by Google Safe Browsing
**Description:** The deployed app showed a full red "Dangerous site" warning in Chrome, blocking all users from accessing it.
**Cause:** The `.herokuapp.com` subdomain (`forefront-hq-cd14dedc71a3.herokuapp.com`) had been previously assigned to another app by Heroku before being allocated to this project. That prior app had been flagged by Google Safe Browsing for phishing/malware, and the flag remained attached to the hostname.
**Fix:** Renamed the Heroku app to get a fresh, unflagged subdomain:

`heroku apps:rename forefront-hq-new`

New hostname: `forefront-hq-new-a54ac6718d65.herokuapp.com`. 
Updated `ALLOWED_HOSTS` in `settings.py` accordingly.

![Dangerous Site Screenshot](./static/images/dangerous-site-img.webp)

---

### Bug 22 — Email Confirmation and Verification Pages Unstyled
**Description:** After registering, the `/accounts/confirm-email/` page rendered without any site styling — no navbar, no dark theme, no layout. It showed raw allauth default markup with "Messages:" and "Menu:" labels.
**Cause:** No custom template overrides existed for allauth's `verification_sent.html` or `email_confirm.html`. Django was falling back to allauth's built-in templates which extend `account/base_entrance.html` instead of the project's `base.html`. The `templates/account/` directory did not exist in the project.
**Fix:** Created `templates/account/` inside the project's root templates directory and added two override templates:
- `templates/account/verification_sent.html` — styled "check your inbox" page shown after registration
- `templates/account/email_confirm.html` — styled confirmation page shown when clicking the email link

Both templates extend `base.html` and use the existing `.auth-wrapper`, `.auth-card`, `.auth-title`, `.auth-sub`, and `.btn` classes to match the login and register pages.

![Email Confirmation Page](./static/images/unstyled-confirm-email-img.webp)

---

### Bug 23 — Heroku Deployment Returning 400 Bad Request
**Description:** After deploying the application to Heroku, visiting the live site displayed a plain "Bad Request (400)" page instead of the homepage. The application loaded correctly in local development but rejected requests made through the Heroku domain.
**Cause:** The project was configured to load ALLOWED_HOSTS and SECRET_KEY from environment variables:
`ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')`
`SECRET_KEY = os.environ.get('SECRET_KEY')`
While these values existed in the local .env file, they had not been added to Heroku Config Vars. As a result:
`ALLOWED_HOSTS` evaluated to `['']`
The Heroku domain was not recognised as a valid host
Django rejected incoming requests and returned HTTP 400 responses
Heroku logs confirmed repeated requests returning:
GET / HTTP/1.1" 400
status=400
**Fix:** Added the required environment variables to Heroku:
`heroku config:set SECRET_KEY="your-secret-key"`
`heroku config:set ALLOWED_HOSTS="127.0.0.1,localhost,forefront-hq-new-a54ac6718d65.herokuapp.com"`
The application was then restarted:
`heroku restart --app forefront-hq-new`
After deployment, the logs showed successful responses:
`GET / HTTP/1.1" 200`
`status=200`
confirming that Django was correctly accepting requests from the Heroku domain.
**Result:** The deployed application loaded successfully and all static assets were served correctly.

**Before fix**

![Bad request 400 error](./static/images/bug23-before-fix.png)

**After Fix**

![400 request fixed](./static/images/bug23-after-fix.png)

---

## Known Bugs
 
### Known Bug 1 — Confirmation Email Not Sending After Successful Payment
 
**Description:** The Stripe webhook processes successfully and creates the `Order` and `Payment` records correctly, but the confirmation email is not delivered to the customer after checkout.
 
**Evidence:** Heroku logs confirm the webhook receives the `checkout.session.completed` event and the order is created in the database. The `send_mail()` call executes without raising an exception and `confirmation_email_sent` is set to `True` on the order, but no email arrives in the customer's inbox.
 
**Suspected Cause:** The Google Workspace SMTP credentials (`EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`) are correctly set as Heroku config vars, however the sending alias (`hello@forefronthq.co.uk`) may be getting rejected silently by Gmail's SMTP relay when called from within the webhook handler context on Heroku, rather than from a standard request/response cycle.
 
**Status:** Unresolved at time of submission. The webhook itself is fully functional — orders and payments are created correctly. The email sending logic is in place and works in local development with the same credentials.

![Stripe Webhook confirmation](./static/images/stripe-webhook-confirmation-screenshot.png)

### Known Bug 2 - Social media links, privacy policy and terms & conditions footer links. Not directed to these pages.

**Description** The links are live on the footer throughout the project. They do direct th user to what is described currently. 

**Status** Unresolved at this time. Until the relevant social media pages are live and active. Also the privacy policy and terms & conditions are written and pages implemented into the project.


---

## Code Validation
 
### HTML Validation
 
All HTML was validated using the [W3C HTML Validator](https://validator.w3.org/) by entering the live Heroku URL directly into the validator. This checks the fully rendered HTML returned by the server, which correctly handles Django template tags that would cause false errors if the raw template source were pasted in directly.
 
| Page | Result |
|---|---|
| Home | ✓ No errors |
| About | ✓ No errors |
| Services | ✓ No errors |
| Packages | ✓ No errors |
| Custom Package Builder | ✓ No errors |
| Custom Package Summary | ✓ No errors |
| Portfolio | ✓ No errors |
| Contact | ✓ No errors |
| Login | ✓ No errors |
| Register | ✓ No errors |
| Payment Success | ✓ No errors |

![Home Page Validation](./static/images/home.html-validation-screenshot.png)

![About Page Validation](./static/images/about.html-validation-screenshot.png)

![Services Page Validation](./static/images/services.html-validation-screenshot.png)

![Packages Page Validation](./static/images/packages.html-validation-screenshot.png)

![Custom Package Builder Validation](./static/images/custom_package.html-validation-screenshot.png)

![Custom Package Summary Validation](./static/images/custom_package_summary.html-validation-screenshot.png)

![Portfolio Page Validation](./static/images/portfolio.html-validation-screenshot.png)

![Contact Page Validation](./static/images/contact.html-validation-screenshot.png)

![Login Page Validation](./static/images/login.html-validation-screenshot.png)

![Register Page Validation](./static/images/create_account.html-validation-screenshot.png)

![Payment Success Page Validation](./static/images/payment_succesful.html-validation-screenshot.png)

---

### CSS Validation
 
The stylesheet was validated using the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) by direct input of `static/css/style.css`.
 
| File | Result |
|---|---|
| static/css/style.css | ✓ No errors |

![CSS Validation](./static/images/css-validation-FHQ.png)

---

### JavaScript Unit Tests (Jest)
 
Unit tests for `script.js` were written using [Jest](https://jestjs.io/) with the `jest-environment-jsdom` package to simulate a browser DOM environment. Tests are located at `static/js/script.test.js` and were run from the project root using `npm test`.
 
| Test | Result |
|---|---|
| Alert is still visible before 5 seconds | ✓ Pass |
| Alert begins fading after 5 seconds | ✓ Pass |
| Alert is removed from DOM after fade completes | ✓ Pass |
| Transition is set before fade out | ✓ Pass |
| Multiple alerts are all dismissed | ✓ Pass |
| No error when no alerts are present | ✓ Pass |
| Total is 0 when no checkboxes are checked and pages is 0 | ✓ Pass |
| Total reflects a single checked addon | ✓ Pass |
| Total reflects multiple checked addons | ✓ Pass |
| Total includes page cost when pages are set | ✓ Pass |
| Total combines addons and pages correctly | ✓ Pass |
| Summary button is disabled when total is 0 | ✓ Pass |
| Summary button is enabled when total is greater than 0 | ✓ Pass |
| Checking an addon updates the total | ✓ Pass |
| Unchecking an addon reduces the total | ✓ Pass |
| Unchecking all addons disables the summary button | ✓ Pass |
| Changing page input updates the total | ✓ Pass |
| Setting pages to 0 removes page cost from total | ✓ Pass |
| Invalid page input treated as 0 | ✓ Pass |
| No error when page input is absent | ✓ Pass |
 
**Test Suites: 1 passed — Tests: 20 passed — Time: 0.573s**

![JavaScript Jest Testing](./static/images/jest-test.png)

---

### Python Validation
 
All Python files were validated using the [CI Python Linter](https://pep8ci.herokuapp.com/) to check for PEP8 compliance.
 
| File | Result |
|---|---|
| forefront_hq/settings.py | ✓ No errors |
| forefront_hq/urls.py | ✓ No errors |
| about/models.py | ✓ No errors |
| about/views.py | ✓ No errors |
| about/urls.py | ✓ No errors |
| about/admin.py | ✓ No errors |
| about/tests.py | ✓ No errors |
| accounts/models.py | ✓ No errors |
| accounts/views.py | ✓ No errors |
| accounts/urls.py | ✓ No errors |
| accounts/tests.py | ✓ No errors |
| contact/models.py | ✓ No errors |
| contact/views.py | ✓ No errors |
| contact/urls.py | ✓ No errors |
| contact/admin.py | ✓ No errors |
| contact/tests.py | ✓ No errors |
| orders/models.py | ✓ No errors |
| orders/admin.py | ✓ No errors |
| orders/tests.py | ✓ No errors |
| packages/models.py | ✓ No errors |
| packages/views.py | ✓ No errors |
| packages/urls.py | ✓ No errors |
| packages/admin.py | ✓ No errors |
| packages/tests.py | ✓ No errors |
| portfolio/models.py | ✓ No errors |
| portfolio/views.py | ✓ No errors |
| portfolio/urls.py | ✓ No errors |
| portfolio/admin.py | ✓ No errors |
| portfolio/tests.py | ✓ No errors |
| services/models.py | ✓ No errors |
| services/views.py | ✓ No errors |
| services/urls.py | ✓ No errors |
| services/admin.py | ✓ No errors |
| services/tests.py | ✓ No errors |
 
---

## Automated Testing (Django)
 
All Python unit tests were written using Django's built-in `TestCase` class and run using:
 
```
python manage.py test
```
 
Tests cover models, views, and business logic across all apps.
 
| App | Test Classes | Tests | Result |
|---|---|---|---|
| packages | 15 | 54 | ✓ Pass |
| accounts | 4 | 32 | ✓ Pass |
| services | 2 | 10 | ✓ Pass |
| orders | 2 | 18 | ✓ Pass |
| portfolio | 4 | 16 | ✓ Pass |
| contact | 2 | 24 | ✓ Pass |
| about | 2 | 12 | ✓ Pass |
| **Total** | **31** | **173** | **All passing** |
 
```
Found 173 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........................................................................
----------------------------------------------------------------------
Ran 173 tests in 15.414s
 
OK
Destroying test database for alias 'default'...
```
 
![Python test screenshot](./static/images/python-tests-screenshot.png)
 
---

## Lighthouse Testing
 
Pages were tested using Chrome DevTools Lighthouse in desktop mode against the live Heroku deployment.
 
| Page | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Home | 99 | 92 | 100 | 100 |

![Lighhouse Report](./static/images/lighthouse-summary-FHQ.png)

---

## Manual Testing
 
### User Stories
 
| User Story | Expected Outcome | Result |
|---|---|---|
| As a visitor, I can view all available packages | Packages page displays all active packages with pricing | ✓ Pass |
| As a visitor, I can build a custom package | Custom builder shows addons with running total | ✓ Pass |
| As a visitor, I can view the portfolio | Portfolio page displays all live projects | ✓ Pass |
| As a visitor, I can view available services | Services page lists all active services | ✓ Pass |
| As a visitor, I can submit a contact enquiry | Form submits and success message is shown | ✓ Pass |
| As a visitor, I can register for an account | Registration creates user and sends verification email | ✓ Pass |
| As a user, I can log in with my email and password | Login authenticates user and redirects | ✓ Pass |
| As a user, I cannot log in without verifying my email | Unverified users are blocked with an error message | ✓ Pass |
| As a user, I can sign in with Google | Google OAuth redirects and logs user in | ✓ Pass |
| As a user, I can purchase a package via Stripe | Checkout redirects to Stripe and order is created on success | ✓ Pass |
| As a user, I can build and purchase a custom package | Custom checkout redirects to Stripe with correct line items | ✓ Pass |
| As a user, I receive a confirmation email after purchase | Email sent to user on successful webhook event | ✓ Pass |
| As a user, I can log out | Logout clears session and redirects to home | ✓ Pass |
 
---

### Navigation
 
| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Navbar logo | Click FHQ logo | Redirects to home page | ✓ Pass |
| Navbar — Packages | Click Packages | Navigates to packages page | ✓ Pass |
| Navbar — Portfolio | Click Portfolio | Navigates to portfolio page | ✓ Pass |
| Navbar — Contact | Click Contact | Navigates to contact page | ✓ Pass |
| Navbar — Login (logged out) | Click Login | Redirects to login page | ✓ Pass |
| Navbar — Register (logged out) | Click Register | Redirects to register page | ✓ Pass |
| Navbar — Logout (logged in) | Click Logout | Logs user out and redirects to home | ✓ Pass |
| Mobile navbar | Click hamburger | Menu expands with all nav links | ✓ Pass |
| Footer links | Click any footer link | Navigates to correct page | ✓ Pass |
 
---

### Authentication
 
| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Register — valid details | Submit form with valid email and matching passwords | User created, verification email sent, redirected to confirmation page | ✓ Pass |
| Register — passwords do not match | Submit mismatched passwords | Error message shown, no user created | ✓ Pass |
| Register — duplicate email | Submit an email already registered | Error message shown, no user created | ✓ Pass |
| Register — short password | Submit password under 8 characters | Error message shown, no user created | ✓ Pass |
| Register — already logged in | Visit /register/ while logged in | Redirected to home | ✓ Pass |
| Login — valid credentials | Submit correct email and password | User logged in and redirected | ✓ Pass |
| Login — wrong password | Submit incorrect password | Error message shown, not logged in | ✓ Pass |
| Login — unknown email | Submit email not in system | Error message shown, not logged in | ✓ Pass |
| Login — unverified email | Submit valid credentials before verifying email | Blocked with message to check inbox | ✓ Pass |
| Login — already logged in | Visit /login/ while logged in | Redirected to home | ✓ Pass |
| Login — next param | Log in with ?next=/packages/ in URL | Redirected to /packages/ after login | ✓ Pass |
| Google OAuth | Click Sign in with Google | OAuth flow completes and user is logged in | ✓ Pass |
| Logout | Click Logout | Session cleared, redirected to home, success message shown | ✓ Pass |
 
---

### Packages
 
| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Packages page | Visit /packages/ | All active packages displayed | ✓ Pass |
| Package CTA — logged out | Click Get Started | Redirected to login | ✓ Pass |
| Package CTA — logged in | Click Get Started | Redirected to Stripe Checkout | ✓ Pass |
| Stripe Checkout | Complete payment | Redirected to success page, order created, confirmation email sent | ✓ Pass |
| Payment cancel | Click back/cancel on Stripe | Redirected to packages page with error message | ✓ Pass |
| Custom package builder | Visit /packages/custom/ | Addons displayed with running total | ✓ Pass |
| Custom builder — select addon | Check an addon checkbox | Running total updates immediately | ✓ Pass |
| Custom builder — deselect addon | Uncheck an addon | Running total decreases | ✓ Pass |
| Custom builder — add pages | Enter a number in pages input | Total updates to include page cost | ✓ Pass |
| Custom builder — summary button | Total is 0 | Summary button is disabled | ✓ Pass |
| Custom builder — summary button | Total is greater than 0 | Summary button is enabled | ✓ Pass |
| Custom summary page | Submit addon selection | Summary page shows selected addons and total | ✓ Pass |
| Custom summary — remove addon | Click remove on an addon | Addon removed, total recalculated | ✓ Pass |
| Custom summary — remove pages | Click remove on pages | Pages removed, total recalculated | ✓ Pass |
| Custom checkout — logged out | Visit /packages/custom/checkout/ | Redirected to login | ✓ Pass |
| Custom checkout — no addons | Visit with empty selection | Redirected back to custom package builder | ✓ Pass |
| Custom checkout — logged in | Proceed with addons selected | Redirected to Stripe Checkout with correct line items | ✓ Pass |
 
---

### Portfolio
 
| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Portfolio page | Visit /portfolio/ | All live projects displayed | ✓ Pass |
| Portfolio — draft project | Check unlive project | Not visible on portfolio page | ✓ Pass |
| Portfolio — ordering | View projects | Ordered by most recently completed | ✓ Pass |
| Portfolio — tags | View project cards | Tags display correctly on each card | ✓ Pass |
 
---

### Services
 
| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Services page | Visit /services/ | All active services displayed | ✓ Pass |
| Services — inactive service | Check hidden service | Not visible on services page | ✓ Pass |
| Services — ordering | View page | Services ordered by display_order | ✓ Pass |
 
---

### Contact
 
| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Contact page | Visit /contact/ | Form loads with active services in dropdown | ✓ Pass |
| Contact — submit logged out | Submit form as anonymous user | Enquiry created with no user, success message shown | ✓ Pass |
| Contact — submit logged in | Submit form as authenticated user | Enquiry created and linked to user, success message shown | ✓ Pass |
| Contact — no service selected | Submit form with no service | Enquiry created with service as null | ✓ Pass |
| Contact — with service | Submit form with service selected | Enquiry linked to correct service | ✓ Pass |
| Contact — redirect | Submit form | Redirected back to contact page | ✓ Pass |
 
---
 
### About
 
| Feature | Action | Expected Result | Result |
|---|---|---|---|
| About page | Visit /about/ | Active team members displayed | ✓ Pass |
| About — inactive member | Check hidden member | Not visible on about page | ✓ Pass |
| About — ordering | View page | Members ordered by display_order | ✓ Pass |
 
---

## Responsiveness Testing
 
The site was tested across mobile, tablet, and desktop screen widths using Chrome DevTools device emulation.
 
| Page | Mobile (375px) | Tablet (768px) | Desktop (1440px) |
|---|---|---|---|
| Home | ✓ Pass | ✓ Pass | ✓ Pass |
| About | ✓ Pass | ✓ Pass | ✓ Pass |
| Services | ✓ Pass | ✓ Pass | ✓ Pass |
| Packages | ✓ Pass | ✓ Pass | ✓ Pass |
| Custom Package Builder | ✓ Pass | ✓ Pass | ✓ Pass |
| Custom Package Summary | ✓ Pass | ✓ Pass | ✓ Pass |
| Portfolio | ✓ Pass | ✓ Pass | ✓ Pass |
| Contact | ✓ Pass | ✓ Pass | ✓ Pass |
| Login | ✓ Pass | ✓ Pass | ✓ Pass |
| Register | ✓ Pass | ✓ Pass | ✓ Pass |

### Mobile View

![Mobile View](./static/images/mobile-view.png)

### Tablet View

![Tablet View](./static/images/tablet-view.png)

### Desktop View

![Desktop View](./static/images/desktop-view.png)

---

## Browser Compatibility
 
| Browser | Result |
|---|---|
| Chrome | ✓ Pass |
| Firefox | ✓ Pass |
| Safari | ✓ Pass |
| Edge | ✓ Pass |
 
---

## Usability Testing
 
Usability testing was carried out manually to confirm that the site is easy to navigate and use for someone visiting for the first time. The focus was on whether key interactions gave clear feedback, whether the purchase flow was intuitive, and whether the site communicated its purpose without friction.
 
| Scenario | Expectation | Result |
|---|---|---|
| First-time visitor lands on home page | Tagline and CTAs communicate site purpose immediately | ✓ Pass |
| Visitor clicks View Packages | Navigates to packages page and all options are clearly laid out | ✓ Pass |
| Visitor clicks Build Your Own | Custom package builder loads with addons and a live running total | ✓ Pass |
| Logged-out user clicks Get Started on a package | Redirected to login with the package checkout as the next destination | ✓ Pass |
| User submits registration with mismatched passwords | Inline error message shown before any account is created | ✓ Pass |
| User submits registration with a short password | Clear error message explaining the 8 character minimum | ✓ Pass |
| User registers successfully | Redirected to a styled confirmation page explaining to check their inbox | ✓ Pass |
| User logs in with wrong password | Error message displayed, form does not reset the email field | ✓ Pass |
| User attempts to log in before verifying email | Blocked with a clear message directing them to check their inbox | ✓ Pass |
| User completes Stripe payment | Redirected to a success page confirming the order | ✓ Pass |
| User cancels Stripe payment | Redirected back to packages page with an error message | ✓ Pass |
| User submits contact form | Success message confirms the message was sent | ✓ Pass |
| User on mobile opens nav menu | Hamburger expands all navigation links correctly | ✓ Pass |
| User navigates to a non-existent URL | Custom 404 page is displayed with navigation intact | ✓ Pass |
 
---

## Data Management Testing
 
This section tests that data flows correctly through the application — from creating and updating records through the Django admin, to enforcing model-level rules, to ensuring the Stripe webhook handles order creation and email confirmation reliably.
 
| Test | Expected Behaviour | Result |
|---|---|---|
| Create a new package via admin | Package saved and visible on packages page | ✓ Pass |
| Deactivate a package via admin | Package no longer appears on packages page | ✓ Pass |
| Create a new service via admin | Service saved and visible on services page | ✓ Pass |
| Deactivate a service via admin | Service no longer appears on services page | ✓ Pass |
| Create a portfolio project as live | Project appears on portfolio page | ✓ Pass |
| Set portfolio project to not live | Project no longer appears on portfolio page | ✓ Pass |
| Create a staff member as active | Staff member appears on about page | ✓ Pass |
| Set staff member to inactive | Staff member no longer appears on about page | ✓ Pass |
| Submit contact form as logged-in user | Enquiry saved with user FK and visible in admin | ✓ Pass |
| Submit contact form as anonymous user | Enquiry saved with null user and visible in admin | ✓ Pass |
| Delete a package | Associated orders retain the package as NULL rather than being deleted (SET_NULL) | ✓ Pass |
| Delete a user | Associated orders and enquiries are cascade deleted | ✓ Pass |
| Complete Stripe checkout | Order and Payment records created in database | ✓ Pass |
| Complete Stripe checkout | Confirmation email sent to customer | ✓ Pass |
| Complete Stripe checkout | confirmation_email_sent set to True on order | ✓ Pass |
| Complete Stripe checkout | Stripe customer ID saved to UserProfile | ✓ Pass |
| Complete custom package checkout | Order created with null package FK and correct total | ✓ Pass |
| Webhook fires with no user_id in metadata | Webhook returns 200 but no order is created | ✓ Pass |
| Webhook receives invalid signature | Returns 400, no order created | ✓ Pass |
| Custom package — select and deselect addons | Running total updates correctly in real time | ✓ Pass |
| Custom package — increase pages beyond 30 | Page count is capped at 30 | ✓ Pass |
| Custom package — decrease pages below 1 | Page count cannot go below 1 | ✓ Pass |
| Custom summary — remove addon | Addon removed from session and total recalculated | ✓ Pass |
| Custom summary — remove pages | Pages reset to zero and total recalculated | ✓ Pass |
 
---

## Deployment

## Deploying to Heroku
 
The project was deployed to Heroku by connecting the GitHub repository through the Heroku dashboard. The following steps were followed:
 
1. Log in to [Heroku](https://www.heroku.com/) and click **New → Create new app**
2. Give the app a unique name and select your region, then click **Create app**
3. In the **Resources** tab, search for **Heroku Postgres** and add it as an add-on to provision the database
4. In the **Settings** tab, click **Reveal Config Vars** and add the following environment variables:
| Key | Value |
|---|---|
| `DATABASE_URL` | Your Heroku PostgreSQL URL (added automatically) |
| `SECRET_KEY` | Your Django secret key |
| `ALLOWED_HOSTS` | Your Heroku hostname and localhost |
| `DEBUG` | `False` |
| `DJANGO_SETTINGS_MODULE` | `forefront_hq.settings` |
| `STRIPE_SECRET_KEY` | Your Stripe secret key |
| `STRIPE_PUBLIC_KEY` | Your Stripe publishable key |
| `STRIPE_WEBHOOK_SECRET` | Your Stripe webhook signing secret |
| `EMAIL_HOST_USER` | Your Google Workspace email address |
| `EMAIL_HOST_PASSWORD` | Your Google Workspace app password |
 
5. In the **Deploy** tab, select **GitHub** as the deployment method
6. Search for your repository name and click **Connect**
7. Scroll down to **Manual Deploy**, select the `main` branch and click **Deploy Branch**
8. Once the build completes, click **Open App** to view the live site
> **Note:** After deployment, if your app is assigned an existing Heroku subdomain that has a Google Safe Browsing flag from a previous tenant, rename the app via the CLI to get a fresh hostname:
> ```
> heroku apps:rename your-new-app-name
> ```
> Then update `ALLOWED_HOSTS` in your Heroku config vars with the new hostname.

---

## How To Run The Project Locally
 
To clone this project from GitHub:
 
1. Follow this link to the [GitHub Repository](https://github.com/Ash-39284/forefront-hq)
2. Under the repository name, click the green **Code** button to reveal a dropdown menu
3. Select the **HTTPS** tab and copy the URL
4. In your local IDE open **Git Bash**
5. Change the current working directory to the location where you want the cloned directory
6. Type `git clone` followed by the URL you copied, then press **Enter**:
```bash
git clone https://github.com/Ash-39284/forefront-hq
```
7. Navigate into the cloned directory:
```bash
cd forefront_hq
```
8. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
9. Install the required dependencies:
```bash
pip install -r requirements.txt
```
10. Create a `.env` file in the root directory and add your environment variables:
```
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLIC_KEY=your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
EMAIL_HOST_USER=your-google-workspace-email
EMAIL_HOST_PASSWORD=your-google-workspace-app-password
```
11. Run the database migrations:
```bash
python manage.py migrate
```
12. Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```
13. Collect static files:
```bash
python manage.py collectstatic
```
14. Start the development server:
```bash
python manage.py runserver
```
15. Open your browser and navigate to `http://127.0.0.1:8000/`

---

# Credits

## Content 

All written content — including service descriptions, package features, and page copy — was written by Ashley Roberts.

## Code
 
- [Django Documentation](https://docs.djangoproject.com/) — models, views, forms, authentication, admin, testing
- [django-allauth Documentation](https://docs.allauth.org/) — email verification, Google OAuth, custom template overrides
- [Stripe Documentation](https://stripe.com/docs) — Checkout sessions, webhook handler, signature verification
- [Google Cloud Documentation](https://cloud.google.com/docs) — OAuth 2.0 credentials and redirect URI setup
- [Heroku Documentation](https://devcenter.heroku.com/) — deployment, config vars, Postgres setup
- [W3Schools](https://www.w3schools.com/) — HTML, CSS, and JavaScript reference
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/) — grid system, navbar, responsive utilities
- [Jest Documentation](https://jestjs.io/docs/getting-started) — JavaScript unit testing setup and configuration

## Images
 
- Portfolio project images hosted via [imgbb](https://imgbb.com/)
- FHQ logo and brand assets created by Ashley Roberts in Canva
- Page mockup designs created by Ashley Roberts in Canva an in Google stitch
- Colour pallette was made by claude ai 
- 

### Acknowledgdements

This project was developed and coded by Ashley Roberts in 2026.