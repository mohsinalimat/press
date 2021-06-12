# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe


def execute():
	frappe.reload_doc("press", "doctype", "cluster")
	for name in frappe.get_all("Cluster", pluck="name"):
		cluster = frappe.get_doc("Cluster", name)
		cluster.save()
