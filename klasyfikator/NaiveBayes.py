# -*- coding: utf-8 -*-

"""Dane klasyfikatora bayesowskiego."""

class NaiveBayes:

    """
    Klasa reprezentująca parametry i stan naiwnego klasyfikatora
    bayesowskiego.
    """

    def __init__(self, get_features):
        self.feature_count = { }
        self.class_count = { }
        self.get_features = get_features
