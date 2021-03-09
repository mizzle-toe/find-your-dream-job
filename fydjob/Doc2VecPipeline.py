#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import json
import os


class DocPipeline:
    def __init__(self, path=None):

        if path:
            self.d2v_model = Doc2Vec.load(path)
        else:
            self.d2v_model = Doc2Vec(dm=0, alpha=0.025, min_count=1)
