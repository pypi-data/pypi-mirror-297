================
News / Changelog
================


.. _news.1.3.12:

1.3.12
======

(2024-09-21)

- Fix the build metadata in pyproject.toml to remove `example_project`
  from wheels. (Fixes #514)


.. _news.1.3.11:

1.3.11
======

(2024-07-03)

- Fix the build metadata in pyproject.toml to include the required
  files for testing in the source distribution.


.. _news.1.3.10:

1.3.10
======

(2024-06-29)

**This release has been yanked from PyPI due to bad build**.

- A coding error causing AttributeError 'Manager' object has no attribute
   'delete' has been fixed.  (Fixes #498)
- Replace Django-Q with `Django-Q2 <https://django-q2.readthedocs.io/en/master/index.html>`_
  since, it is not maintained and compatible with new Django version (Fixes #493)
- A MultipleObjectsReturned exception in checking if a thread is read is now
  caught and handled.  (Fixes #500)
- Avoid some crashes whith hyperkitty_import (See !615)
- Do not escape email addresses on export (Fixes #507)
- Replaced django.utils.timezone.utc with datetime.timezone.utc for Django 5.0
  compatibility.  (Fixes #509)

.. _news-1.3.9:

1.3.9
=====

(2024-02-27)

- Handle the case when a user posting from Hyperkitty is banned in the
  list.  (Fixes #325)
- Instead of defaulting to replying via Email software, provide option
  to login and reply for un-authenticated users too.  (Fixes #277)
- Tags count really doesn't add anything to the page since it isn't
  expected to be too many like authors/messages.  (Fixes #43)
- 'Start a new thread' will redirect to login if the user is not
  logged in, instead of disabling it.  (Fixes #50)
- List owners can now delete messages and threads and reattach threads.
  (Fixes #261)
- Archive rendering no longer removes backslash escapes.  (Closes #490)
- Add support for mistune 3.x, making dependency on mistune>=3.0.
- Fix the rendering of contents of blockquote in plaintext rendering
  mode.  (See #393)
- Fixes the rendering of patches in markdown rendering mode.  (Fixes #393)
- Replace use of ``pytz`` with ``zoneinfo``.  (See !462)
- An attachment with content ``None`` is properly handled.  (Closes #496)
- Fix a bug which caused error in plaintext renderer when the
  email was quoted more than default no of. max_nested_levels
  in mistune. (Fixes #494)

.. _news-1.3.8:

1.3.8
=====

(2023-10-21)

 - Make it compatible with elasticsearch 8.0.0
 - Removed unnecessary SESSION_SERIALIZER from settings.py.  (Closes #455)
 - Updated the contrib/check_hk_import script to catch more issues.
 - Update API Views to use LimitOffsetPagination as the default pagination
   style. (Fix #457)
 - Added a new contrib/cleanarch3 script it check/fix mboxes for unescaped
   "From " lines and bad Date: headers.
 - Upgrade to Bootstrap 5 and the UI redesign. (See !498)
 - Add support for Django 4.2
 - hyperkitty_import no longer fails with recent Python and Message-ID: <>
   (Closes #396)
 - Add support to parse outlook style replies so they can be hidden inside
   a quote section like regular quoted replies. (Fixes #478)
 - Change color for 4th level quoted text. (Fixes #354)
 - Fixed an issue in hyperkitty_import in trying to apply .strip() to a
   email.header.Header object.  (Fixes #480)

A11y
----

 - Use nav pills in the user profile page to be consistent with rest of
   the pages and update the aria-role of the navigation. (See #464)
 - Re-add the search button so it is more accessible and users don't have
   to guess that you need to press enter to search. Also, add the aria
   label for the search button. (Fixes #362)
 - Use better heading hierarchy and update styling to make sure the look
   does not change. (Fixes #373)
 - Add more headings to the thread page for easier navigation using assistive
   technologies. (Fixes #370)
 - Make the active sort-mode also clickable so that keyboard focus can land
   on it and it can be announced. Also, add aria labels to announce the
   currently selected one as active page. (Fixes #365)
 - Add ARIA labels to the like and dislike buttons. (Fixes #363)
 - Add ARIA labels to icons on overview page in thread summary. (Fixes #364)
 - Add ARIA label to the search input in the top navigation bar. (Fixes #361)
 - Add sections and aria labels to input and navigation and aria-autocomplete
   to search list form on index page. (Fixes #366)
 - Fix the tab ordering of the next/older threads in the thread page.
   (Fixes #369)
 - Fix the toggle fixed-font button so it can receive keyboard focus.
 - Simplified like/dislike UI, smiley face replaced by thumbs up/down.
   (Fixes #44)

.. _news-1.3.7:

1.3.7
=====

(2023-01-04)

- ``hyperkitty_import`` will now import messages to a list with archiving
  disabled.  (Closes #451)
- Add support for Python 3.11.


.. _news-1.3.6:

1.3.6
=====

(2022-10-22)

- Fixed an issue in hyperkitty_import with an empty Message-ID.  (Closes #396)
- Set Q_CLUSTER retry > timeout in example_project.  (Closes #402)
- Set DEFAULT_AUTO_FIELD to silence errors with Django >= 3.2.
- Require mistune >= 2.0.0 and fix a problem with importing from it. (Closes #395)
- Adapt parsing of emails to be compatible with python 3.10. (Closes #401)
- Add gitlab-ci integration for python 3.10.
- Skip lists with private archives in the find list search. (Closes #237)
- Add a new setting ``HYPERKITTY_MBOX_EXPORT`` which, when set to false,
  removes the :guilabel:`Download` button and disables the export view. (
  Fixes #386)
- Return 400 instead of 500 when the sort mode is invalid. (Fixes #270)
- Allow HyperKitty to find attachments in either the database or the
  ``HYPERKITTY_ATTACHMENT_FOLDER``.  (Closes #213)
- Implemented a new ``attachments_to_file`` management command to move
  attachment content to the file system after setting
  ``HYPERKITTY_ATTACHMENT_FOLDER``.  (Closes #413)
- Handle exception when a banned address tries to post. (Fixes #325)
- Add an index on the 'name' column (fqdn)for the MailingList table since it is
  most frequently used to query the MailingList object.
- Add the ability to view a thread without Javascript enabled. This uses the
  same mechanism we use with bot-detection and rendering of the entire page at
  once, which will be slow to load but allow reading. (See #422)
- Improve the performance of the thread view for logged-in users by optimizing
  the total database calls made. (See !409)
- Add support for Django <= 4.1
- Remove support for Django < 3.2
- Remove support for Python 3.6
- Fix tests to be compatible with Python 3.10
- Replace use of ``mock`` with ``unittest.mock`` in all tests. (Closes #429)
- The check for writability of ``HYPERKITTY_ATTACHMENT_FOLDER`` when set has
  been improved to avoid a potential race condition.  (Closes #389)

Third Party
-----------

- Bump Jquery-ui to 1.13.1 to fix the broken search. (Closes #411)

UI
--

- Change the design of the thread list page and some minor tweaks
  to the index page. (See !398)
- Remove the counter in the "Top posters" section and all the list of threads
  in the list of overview page. (Fixes #31)


Misc
----

- Use Pytest as the test runner.


.. _news-1.3.5:

1.3.5
=====

(2021-10-12)

- Added feed for mailing lists with an option to configure the number of items
  in those feeds using ```HYPERKITTY_MLIST_FEED_LENGTH``` which defaults to 30
- Print a warning message when skipping older emails during
  ``hyperkitty_import`` execution. (Closes #304)
- Remove links to google fonts (Closes #344)
- Scrubbed messages now have null bytes removed. (Fixed in django-mailman3)
  (Closes #346)
- Add support for rendering Emails as rich text using Markdown parsing rules. (
  See !324)
- Use markdown renderer based on MailingList settings. (Closes #352)
- Mangle lines starting with ``From`` when exporting mbox. (Closes #348)
- Let tasks for non-existent mailing lists fail gracefully.
- ``hyperkitty_import`` now does clean-up of incoming Message-ID headers.
  (Closes #382)
- The ``Email.as_message()`` method removes some bogus characters from the
  Message-ID.  (Closes #383)
- Bump jQuery to 3.6.0.
- Selecting threads by month now works on non-English mobile devices.
  (Closes #384)
- Replace control characters in RSS feed with HTML entities.  (Closes #388)

Security
--------

- Importing a private mailing list with ``hyperkitty_import`` will enforce
  the visibility of the archives for the duration of the import. This fixes
  a bug where the private archives would have public visibility during imports
  which could lead to temporary information leakage.
  (CVE-2021-33038, Closes #380)
- Check the secret archiver key in a way that is resistant to timing attacks.
  (CVE-2021-35057, Closes #387)
- Pass the secret archiver key in a HTTP Authorization header instead of a GET
  query parameter so it doesn't appear in logs. (CVE-2021-35058, Closes #387)
- Fix a vulnerability added in !320, which exposes the archives of Private
  Mailing lists through the new RSS Feeds API due to missing authn/authz checks
  in the new view. (See !362)


.. _news-1.3.4:

1.3.4
=====

(2021-02-02)

- Sync owners and moderators from Mailman Core for MailingList. (Fixes #302)
- Implemented a new ``HYPERKITTY_JOBS_UPDATE_INDEX_LOCK_LIFE`` setting to set
  the lock lifetime for the ``update_and_clean_index`` job.  (Closes #300)
- Implemented a new ``HYPERKITTY_ALLOW_WEB_POSTING`` that allows disabling the
  web posting feature. (Closes #264)
- Add the ability to disable Gravatar using ``HYPERKITTY_ENABLE_GRAVATAR``
  settings. (Closes #303)
- Replaced deprecated ``ugettext`` functions with ``gettext``. (Closes #310)
- Fix export of Email message where the ``In-Reply-To`` header doesn't include
  the ``<>`` brackets. (Closes #331)
- We now catch a few more exceptions in ``hyperkitty_import`` when getting
  messages from a mbox. (Closes #313 and #314)
- Added a new contrib/check_hk_import script to check mboxes before running
  hyperkitty_import.
- We now ignore a ``ValueError`` in ``hyperkitty_import`` when trying to
  replace a ``Subject:`` header. (Closes #317)
- ``hyperkitty_import`` now includes the mbox name in error messages when
  importing multiple mboxes. (Closes #318)
- `` at `` is now only replaced with ``@`` in ``From:`` header values when
  necessary and not unconditionally. (Closes #320)
- The wildcard notation for any host ``'*'`` is now supported into
  ``MAILMAN_ARCHVER_FROM`` to disable Hyperkitty clients IP checking.
- Join the searchbar and search button  like it was before bootstrap 4
  migration. (See !301)
- Use the umd builds for popper.js instead of the regular ones. (See !309)
- Exceptions thrown by smtplib in sending replies are now caught and give an
  appropriate error message.  (Closes #309)

.. _news-1.3.3:

1.3.3
=====

(2020-06-01)

- Allow ``SHOW_INACTIVE_LISTS_DEFAULT`` setting to be configurable. (Closes #276)
- Fix a bug where the user couldn't chose the address to send reply or new post
  as. (Closes #288)
- Improve the Django admin command reference from hyperkitty_import.
  (Closes #281)
- Fix ``FILTER_VHOST`` to work with web hosts other than the email host.
  (Closes #254)
- Fixed a bug where ``export`` can fail if certain headers are wrapped.
  (Closes #292)
- Fixed ``hyperkitty_import`` to allow odd line endings in a folded message
  subject.  (Closes #280)
- Fixed a bug that could throw an ``IndexError`` when exporting messages.
  (Closes #293)
- Use ``errors='replace'`` when encoding attachments.  (Closes #294)

1.3.2
=====

(2020-01-12)

- Remove support for Django 1.11. (Closes #273)
- Skip ``Thread.DoesNotExist`` exception when raised within
  ``rebuild_thread_cache_votes``. (Closes #245)
- Send 400 status code for ``ValueError`` when archiving. (Closes #271)
- Fix a bug where exception for elasticsearch backend would not be caught. (Closes #263)

1.3.1
=====

(2019-12-08)

- Add support to delete mailing list. (Closes #3)
- Fix a bug where messages with attachments would skip adding the body when
  exporting the email. (Closes #252)
- Fix a bug where exporting mbox with messages that have attachments saved
  to disk would raise exception and return a corrupt mbox. (Closes #258)
- Fix a bug where downloaded attachments are returned as a memoryview object
  instead of bytes and hence fail to download. (Closes #247)
- Fix a bug where migrations would fail with exceptions on postgresl. (Closes
  #266)
- Add support for Django 3.0.
- Add support for Python 3.8 with Django 2.2.


1.3.0
=====
(2019-09-04)

- Unread messages now have a blue envelope icon, instead of a gray one before to
  to make them more visible.
- Quoted text in emails have different visual background to improve readability.
- Quoted text is now visually quoted to 3 levels of replies with different visual
  background to improve readability.
- Add a new "All Threads" button in MailingList overview page to point to all the
  the threads in reverse date order. This should give a continuous list of threads.
- Fixes a bug where "All Threads" button leads to 500 page if there aren't any
  threads. (Closes #230)
- Add support for Django 2.2.
- Fix a bug where bad Date header could cause ``hyperkitty_import`` to exit with
  ``TypeError`` due to bad date type.
- Change the Overview page to remove the List of months from left side bar and
  convert different thread categories into tabs.
- Replace unmaintained ``lockfile`` dependency with ``flufl.lock``.
- Remove ``SingletonAsync`` implementation of ``AsyncTask`` and use the upstream
  version for better maintenance.
- Run update_index job hourly by default instead of minutely for performance
  reasons of whoosh.
- Email body now preserves leading whitespaces on lines and wraps around line
  boundary. (Closes #239)
- Do not indent replies on small screens. (Closes #224)
- Add a keyboard shortcut ``?`` to bring up list of keyboard shortcuts.
	(Closes #240)

1.2.2
=====
(2019-02-22)

- ``paintstore`` is no longer a dependency of Hyperkitty. This change requires
  that people change their ``settings.py`` and remove ``paintstore`` from
  ``INSTALLED_APPS``. (See #72)
- Folded Message-ID headers will no longer break threading.  (#216)
- MailingList descriptions are no longer a required field. This makes HyperKity
  more aligned with Core. (Closes #211)


1.2.1
=====
(2018-08-30)

- Several message defects that would cause ``hyperkitty_import`` to abort will
  now just cause the message to be skipped and allow importing to continue.
  (#183)
- If an imported message has no Date: header, ``hyperkitty_import`` will now
  look for Resent-Date: and the unixfrom date before archiving the message
  with the current date.  (#184)
- Add support for Django 2.1. Hyperkitty now supports Django 1.11-2.1 (#193)


1.2.0
=====
(2018-07-10)

- Handle email attachments returned by Scrubber as bytes or as strings with
  no specified encoding. (#171)
- Remove robotx.txt from Hyperkitty. It wasn't working correctly anyway.
  If you still need it, serve it from the webserver directly. (#176)
- Add the possibility to store attachments on the filesystem, using the
  ``HYPERKITTY_ATTACHMENT_FOLDER`` config variable.
- If a message in the mbox passed to ``hyperkitty_import`` is missing a
  ``Message-ID``, a generated one will be added. (#180)
- There is a new management command ``update_index_one_list`` to update the
  search index for a single list. (#175)


1.1.4
=====
(2017-10-09)

- Use an auto-incrementing integer for the MailingLists's id.
  **WARNING**: this migration will take a very long time (hours!) if you have
  a lot of emails in your database.
- Protect a couple tasks against thread and email deletion
- Improve performance in the cache rebuilding async task
- Drop the ``mailman2_download`` command. (#148)
- Adapt to the newest mailmanclient version (3.1.1).
- Handle the case when a moderated list is opened and there are pending
  subscriptions. (#152)
- Protect export_mbox against malformed URLs. (#153)


1.1.1
=====
(2017-08-04)

- Fix the Javascript in the overview page
- Make two Django commands compatible with Django >= 1.10
- Fix sorting in the MailingList's cache value
- Don't show emails before they have been analyzed
- Fix slowdown with PostgreSQL on some overview queries


1.1.0
=====
(2017-05-26)

- Add an async task system, check out the installation documentation to run the necessary commands.
- Support Django < 1.11 (support for 1.11 will arrive soon, only a dependency is not compatible).
- Switch to the Allauth login library
- Performance optimizations.
- Better REST API.
- Better handling of email sender names.
- Improve graphic design.


1.0.3
=====
(2015-11-15)

- Switch from LESS to Sass
- Many graphical improvements
- The SSLRedirect middleware is now optional
- Add an "Export to mbox" feature
- Allow choosing the email a reply or a new message will be sent as


0.9.6
=====
(2015-03-16)

* Adapt to the port of Mailman to Python3
* Merge KittyStore into HyperKitty
* Split off the Mailman archiver Plugin in its own module: mailman-hyperkitty
* Compatibility with Django 1.7


0.1.7
=====
(2014-01-30)

Many significant changes, mostly on:
* The caching system
* The user page
* The front page
* The list overview page


0.1.5
=====
(2013-05-18)

Here are the significant changes since 0.1.4:

* Merge and compress static files (CSS and Javascript)
* Django 1.5 compatibility
* Fixed REST API
* Improved RPM packaging
* Auto-subscribe the user to the list when they reply online
* New login providers: generic OpenID and Fedora
* Improved page loading on long threads: the replies are loaded asynchronously
* Replies are dynamically inserted in the thread view


0.1.4
=====
(2013-02-19)

Here are the significant changes:

* Beginning of RPM packaging
* Improved documentation
* Voting and favoriting is more dynamic (no page reload)
* Better emails display (text is wrapped)
* Replies are sorted by thread
* New logo
* DB schema migration with South
* General style update (Boostream, fluid layout)


0.1 (alpha)
===========
(2012-11-22)

Initial release of HyperKitty.

* login using django user account / browserid / google openid / yahoo openid
* use Twitter Bootstrap for stylesheets
* show basic list info and metrics
* show basic user profile
* Add tags to message threads
