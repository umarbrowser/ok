#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=no-member, no-init, too-many-public-methods
# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring, unused-import, invalid-name, import-error, super-on-old-class
"""Tests for final submissions."""

import os
os.environ['FLASK_CONF'] = 'TEST'
import datetime

from test_base import APIBaseTestCase, unittest

from app import models, utils

from google.appengine.ext import ndb
from google.appengine.ext import deferred
from google.appengine.ext import testbed

class FinalSubmissionTest(APIBaseTestCase):
    def get_accounts(self):
        """
        Returns the accounts you want to exist in your system.
        """
        keys = ["student0", "student1", "student2", "staff", "admin"]
        return {key: models.User(email=[key+"@b.edu"]) for key in keys}

    def setUp(self):
        super(APIBaseTestCase, self).setUp()
        self.accounts = self.get_accounts()
        for user in self.accounts.values():
            user.put()

        self.courses = {
            "first": models.Course(
                institution="UC Awesome",
                display_name="First Course",
                instructor=[self.accounts['admin'].key]),
            "second": models.Course(
                institution="UC Awesome",
                display_name="Second Course",
                instructor=[self.accounts['admin'].key]),
            }

        for course in self.courses.values():
            course.put()

        self.assignments = {
            "first": models.Assignment(
                name="first",
                points=3,
                creator=self.accounts["admin"].key,
                course=self.courses['first'].key,
                display_name="first display",
                templates="{}",
                max_group_size=3,
                due_date=datetime.datetime.now()
                ),
            }
        for assign in self.assignments.values():
            assign.put()
        self.assign = self.assignments["first"]

        # Allow manual execution of deferred tasks using run_deferred
        # https://cloud.google.com/appengine/docs/python/tools/localunittesting
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_taskqueue_stub()

    def run_deferred(self):
        """Execute all deferred tasks."""
        task_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
        for task in task_stub.get_filtered_tasks():
            deferred.run(task.payload)

    def test_one_final(self):
        """An invite/accept/exit/invite sequence keeps a final submission."""
        self.user = self.accounts['student0']

        # Submit
        messages = {'file_contents': {'submit': True, 'trends.py': 'hi!'}}
        self.post_json('/submission', data={'assignment': self.assign.name,
                                            'submitter': self.user.key.id(),
                                            'messages': messages})
        self.run_deferred()

        finals = list(models.FinalSubmission.query().fetch())
        self.assertEqual(1, len(finals))
        final = finals[0]
        # TODO Not sure how to make/verify this final_submission get request...
        # self.assertEqual(final, self.user.get_final_submission(self.assign))
        # self.get('/user/{}/final_submission'.format(self.user.email[0]),
        #          data={'assignment': self.assign.key.id()})

        # Invite
        invited = self.accounts['student1']
        # TODO This post is being made with admin as the user; not sure why...
        self.post_json('/assignment/{}/invite'.format(self.assign.key.id()),
                       data={'email': invited.email[0]})
        # TODO Check final submissions

        # Accept
        # TODO

        # Exit
        # TODO

        # Invite
        # TODO

if __name__ == "__main__":
    unittest.main()