.. |br| raw:: html

    <br />

===============================
Single Responsibility Principle
===============================

Ignacy Sokołowski


----


What is the SRP?
================

Every class, method, function should be **responsible** for only **one** thing.


----


Origin
======

Robert C. Martin a.k.a. Uncle Bob, *Principles of Object Oriented Programming*

Part of **SOLID** principles.

* **S**\ RP – **Single Responsibility Principle**
* **O**\ CP – Open/Closed Principle
* **L**\ SP – Liskov Substitution Principle
* **I**\ SP – Interface Segregation Principle
* **D**\ IP – Dependency Inversion Principle


----


Real life examples
==================

.. rst-class:: build

* A car
* A company
* MVC web frameworks


----


What is the *single responsibility*?
====================================

What does it mean to be **responsible for only one thing**?


----


Not just *doing only one thing*
===============================

It will always do more than one thing.

One function can invoke several other functions |br|
but it will **not** be **responsible** for **how** they are implemented.


----


.. rst-class:: before-no-transition

One level of abstraction
========================

* Send e-mail report

  * Get report data
  * Format the report
  * Send it via e-mail


----


.. rst-class:: no-transition

One level of abstraction
========================

* Send e-mail report

  * Get report data

    * Build an SQL query
    * Send the query to a database
    * Parse the results on data objects

  * Format the report

    * ...
    * ...

  * Send it via e-mail

    * Build an e-mail message
    * Connect to an SMTP server
    * Send the message


----


One level of abstraction
========================

.. code-block:: python

    def send_email_report(user, category, time_period):
        data = get_report_data(category, time_period)
        report_body = format_report(data)
        send_email(user.email, report_body)


----


One reason to change
====================

If you'd like to change the way reports are **formatted**, |br|
you should not need to change the class responsible for **preparing the report
data**.

If you'd like to change the **database** for articles, |br|
you should not need to change the **controller** for displaying articles.


----


Advantages
==========

.. rst-class:: build

* **Readability**. Easier to focus on one responsibility. You name the
  responsibility.
* **Maintainability**. Smaller risk to break a thing when changing another one.
* **Reusability**. An object can be used in many different contexts.
* **Testability**. Easier to test in isolation.


----


Testing
=======

If it does more than one thing, you need to write lots of different tests for
it.

Each test executes the whole body. It **takes time**. Or you need to **mock a
lot**.

**You don't** write sufficent amount of tests simply because it's **too much
testing**.


----


Code smells
===========

* Long function/method
* Long name
* Too many methods in a class
* Too many attributes (cohesion)
* Too many indentation levels
* Too many locals
* Hard to unit test in isolation
* Long test
* Object and data structure at the same time
* Sections within functions
* Comments in code
* Mixed languages


----


Code smell: Too many locals
===========================

.. code-block:: python

    def validate_signature(xml, developer, app, secret):
        timestamp = get_xpath(xml, './Timestamp/text()')
        sig = ''.join([timestamp, developer, app, secret])
        md5sig = hashlib.md5(sig.encode()).digest()
        b64sig = base64.b64encode(md5sig).decode()
        xml_sig = get_xpath(xml, './Signature/text()')
        if xml_sig != b64sig:
            raise SignatureError('XML signature is invalid.')


----


Code smell: Sections within functions
=====================================

.. code-block:: python

    def validate_signature(xml, developer, app, secret):
        timestamp = get_xpath(xml, './Timestamp/text()')
        xml_sig = get_xpath(xml, './Signature/text()')

        sig = ''.join([timestamp, developer, app, secret])
        md5sig = hashlib.md5(sig.encode()).digest()
        b64sig = base64.b64encode(md5sig).decode()

        if xml_sig != b64sig:
            raise SignatureError('XML signature is invalid.')


----


Code smell: Comments in code
============================

.. code-block:: python

    def validate_signature(xml, developer, app, secret):
        timestamp = get_xpath(xml, './Timestamp/text()')
        xml_sig = get_xpath(xml, './Signature/text()')

        # Calculate valid signature.
        sig = ''.join([timestamp, developer, app, secret])
        md5sig = hashlib.md5(sig.encode()).digest()
        b64sig = base64.b64encode(md5sig).decode()

        if xml_sig != b64sig:
            raise SignatureError('XML signature is invalid.')


----


Extracting responsibility
=========================

.. code-block:: python

    def validate_signature(xml, developer, app, secret):
        timestamp = get_xpath(xml, './Timestamp/text()')
        xml_sig = get_xpath(xml, './Signature/text()')
        valid_sig = calculate_valid_signature(timestamp, developer, app, secret)
        if xml_sig != valid_sig:
            raise SignatureError('XML signature is invalid.')


    def calculate_valid_signature(timestamp, developer, app, secret):
        sig = ''.join([timestamp, developer, app, secret])
        md5sig = hashlib.md5(sig.encode()).digest()
        return base64.b64encode(md5sig).decode()


----


Code smell: Mixing objects and data structures
==============================================

.. code-block:: python

    class User(object):

        # [...]

        def send_report(self, category, start_date, end_date):
            email_subject = '{} report for {} - {}'.format(
                category,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
            )
            offers = db_session.query(Offer).filter(
                Offer.category == category,
                Offer.when_created.between(start_date, end_date),
            ).order_by(
                Offer.when_created.desc(),
            ).all()
            template_path = 'report_{}.html'.format(self.report_type)
            template_context = {
                'user': self,
                'category': category,
                'offers': offers,
                'start_date': start_date,
                'end_date': end_date,
            }
            email_body = render_template(template_path, template_context)
            email_message = email.Message(email_subject, email_body)
            smtp = smtplib.SMTP(config.smtp_uri)
            smtp.sendmail(config.sender_email, self.email, email_message.as_string())


----


Code smell: Long method
=======================

.. code-block:: python

    class EmailReporter(object):

        def send_report(self, user, category, start_date, end_date):
            email_subject = '{} report for {} - {}'.format(
                category,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
            )
            offers = db_session.query(Offer).filter(
                Offer.category == category,
                Offer.when_created.between(start_date, end_date),
            ).order_by(
                Offer.when_created.desc(),
            ).all()
            template_path = 'report_{}.html'.format(user.report_type)
            template_context = {
                'user': user,
                'category': category,
                'offers': offers,
                'start_date': start_date,
                'end_date': end_date,
            }
            email_body = render_template(template_path, template_context)
            email_message = email.Message(email_subject, email_body)
            smtp = smtplib.SMTP(config.smtp_uri)
            smtp.sendmail(config.sender_email, user.email, email_message.as_string())


----


Long method refactoring: DTO
============================

.. code-block:: python

    class Report(object):

        def __init__(self, user, category, offers, period):
            self.user = user
            self.category = category
            self.offers = offers
            self.period = period

.. code-block:: python

    class Period(object):

        def __init__(self, start, end):
            self.start = start
            self.end = end

        def __str__(self):
            return '{} - {}'.format(
                self.start.strftime('%Y-%m-%d'),
                self.end.strftime('%Y-%m-%d'),
            )


----


Long method refactoring
=======================

.. code-block:: python

    class ReportPreparator(object):

        def __init__(self, offers_finder):
            self._offers_finder = offers_finder

        def prepare(self, user, category, period):
            offers = self._offers_finder.find(category, period)
            return Report(user, category, offers, period)


----


Long method refactoring
=======================

.. code-block:: python

    class OffersFinder(object):

        def find(self, category, period):
            return db_session.query(Offer).filter(
                Offer.category == category,
                Offer.when_created.between(period.start, period.end),
            ).order_by(
                Offer.when_created.desc(),
            ).all()


----


Long method refactoring
=======================

.. code-block:: python

    class EmailReporter(object):

        def __init__(self, report_preparator):
            self._report_preparator = report_preparator

        def send_report(self, user, category, period):
            email_subject = '{} report for {}'.format(category, period)
            report = self._report_preparator.prepare(user, category, period)
            template_path = 'report_{}.html'.format(user.report_type)
            template_context = {
                'user': report.user,
                'category': report.category,
                'offers': report.offers,
                'period': report.period,
            }
            email_body = render_template(template_path, template_context)
            email_message = email.Message(email_subject, email_body)
            smtp = smtplib.SMTP(config.smtp_uri)
            smtp.sendmail(config.sender_email, user.email, email_message.as_string())


----


Long method refactoring
=======================

.. code-block:: python

    class HTMLReportFormatter(object):

        def format(self, report):
            template_path = 'report_{}.html'.format(report.user.report_type)
            template_context = {
                'user': report.user,
                'category': report.category,
                'offers': report.offers,
                'period': report.period,
            }
            return render_template(template_path, template_context)


----


Long method refactoring
=======================

.. code-block:: python

    class EmailReporter(object):

        def __init__(self, report_preparator, report_formatter):
            self._report_preparator = report_preparator
            self._report_formatter = report_formatter

        def send_report(self, user, category, period):
            email_subject = '{} report for {}'.format(category, period)
            report = self._report_preparator.prepare(user, category, period)
            email_body = self._report_formatter.format(report)
            email_message = email.Message(email_subject, email_body)
            smtp = smtplib.SMTP(config.smtp_uri)
            smtp.sendmail(config.sender_email, user.email, email_message.as_string())


----


Long method refactoring
=======================

.. code-block:: python

    class ReportEmailPreparator(object):

        def __init__(self, report_formatter):
            self._report_formatter = report_formatter

        def prepare(self, report):
            subject = self._prepare_subject(report)
            body = self._report_formatter.format(report)
            return email.Message(subject, body)

        def _prepare_subject(self, report):
            return '{} report for {}'.format(report.category, report.period)


----


Long method refactoring
=======================

.. code-block:: python

    class EmailReporter(object):

        def __init__(self, report_preparator, report_email_preparator):
            self._report_preparator = report_preparator
            self._report_email_preparator = report_email_preparator

        def send_report(self, user, category, period):
            report = self._report_preparator.prepare(user, category, period)
            email_message = self._report_email_preparator.prepare(report)
            smtp = smtplib.SMTP(config.smtp_uri)
            smtp.sendmail(config.sender_email, user.email, email_message.as_string())


----


Long method refactoring
=======================

.. code-block:: python

    class EmailSender(object):

        def __init__(self, smtp_uri, sender_address):
            self._smtp_uri = smtp_uri
            self._sender_address = sender_address

        def send(self, address, message):
            smtp = smtplib.SMTP(self._smtp_uri)
            smtp.sendmail(self._sender_address, address, message.as_string())


----


Long method refactored
======================

.. code-block:: python

    class EmailReporter(object):

        def __init__(self, report_preparator, report_email_preparator, email_sender):
            self._report_preparator = report_preparator
            self._report_email_preparator = report_email_preparator
            self._email_sender = email_sender

        def send_report(self, user, category, period):
            report = self._report_preparator.prepare(user, category, period)
            email_message = self._report_email_preparator.prepare(report)
            self._email_sender.send(user.email, email_message)


Splitting long methods into smaller classes
===========================================

* ``User``
* ``Report``
* ``Period``
* ``EmailReporter``
* ``ReportPreparator``
* ``OffersFinder``
* ``HTMLReportFormatter``
* ``ReportEmailPreparator``
* ``EmailSender``


----


Code smell: Too many methods in a class
=======================================

.. code-block:: python

    class User(object):

        # [...]

        def send_report(self):
            pass

        def prepare_report(self):
            pass

        def make_report_email_message(self):
            pass

        def make_report_email_message_subject(self):
            pass

        def make_report_email_message_body(self):
            pass

        def render_report_email_template(self):
            pass

        def get_report_email_template_path(self):
            pass

        def get_report_email_template_context(self):
            pass

        def get_offers_for_report(self):
            pass

        def get_offers_search_query_for_report(self):
            pass

        def send_email(self):
            pass

        # [...]


----


Code smell: Too many indentation levels
=======================================

.. code-block:: python

    def write_lines(self, lines, encoding=None, errors='strict',
                    linesep=os.linesep, append=False):
        if append:
            mode = 'ab'
        else:
            mode = 'wb'
        f = self.open(mode)
        try:
            for line in lines:
                isUnicode = isinstance(line, unicode)
                if linesep is not None:
                    # Strip off any existing line-end and add the
                    # specified linesep string.
                    if isUnicode:
                        if line[-2:] in (u'\r\n', u'\x0d\x85'):
                            line = line[:-2]
                        elif line[-1:] in (u'\r', u'\n',
                                           u'\x85', u'\u2028'):
                            line = line[:-1]
                    else:
                        if line[-2:] == '\r\n':
                            line = line[:-2]
                        elif line[-1:] in ('\r', '\n'):
                            line = line[:-1]
                    line += linesep
                if isUnicode:
                    if encoding is None:
                        encoding = sys.getdefaultencoding()
                    line = line.encode(encoding, errors)
                f.write(line)
        finally:
            f.close()


----


Code smell: Mixed languages
===========================

.. code-block:: python

    def article_controller(request):
        article_id = request.GET['id']
        article = get_article(article_id)
        return (
            '<html><head><title>{article.title}</title></head>'
            '<body><h1>{article.title}</h1>{article.content}</body></html>'
        ).format(article=article)

.. code-block:: python

    def article_controller(request):
        article_id = request.GET['id']
        article = get_article(article_id)
        css_class = 'new' if article.is_new else ''
        context = {'article': article, 'class': css_class}
        return render_template('article.html', context)

.. code-block:: python

    def article_controller(request):
        article_id = request.GET['id']
        article = cursor.execute(
            'SELECT * FROM articles WHERE id = %s', article_id
        ).fetchone()
        return render_template('article.html', {'article': article})


----


Summary
=======

* Split responsibility into multiple classes/functions/methods
* Hide lower level in a private method if it really belongs to the class
* Extract data structures into separate classes (DTO)
* Use dependency injection


----


Thank you
=========

* Twitter: `@ignacy <https://twitter.com/ignacy>`_
* Github: `ignacysokolowski <https://github.com/ignacysokolowski>`_
* E-mail: ignacy.sokolowski@gmail.com
