#!/usr/bin/env python

from collection import Collection, Scorer
from random import randint
from clustering import Partition
from distance_matrix import DistanceMatrix
from lib.remote.externals.phyml import Phyml

class emtrees(object): 

    # Not sure if scorer required
    # Possible end criteria?

    def __init__(
        self, 
        collection, 
        nclusters, 
        metric = 'euc',
        method='distance',
        ): 

        if not isinstance(nclusters, int) or nclusters <= 1:
            raise Exception('Need appropriate value for number of clusters.')

        self.nclusters = nclusters
        self.scorer = Scorer(collection.records, collection.analysis) # Could check for entries
        self.datatype = collection.datatype
        self.tmpdir = collection.tmpdir
        self.method = method
        self.metric = metric
        self.assign_clusters()

    def assign_clusters(self):
        # Collapse equivalent trees?
        k = self.nclusters
        self.partition = Partition( [randint(1,k) for rec in self.scorer.records] )
        self.L = self.scorer.score(self.partition)

    def maximise(self): # Needs to change
        count = 0
        # clusters = [ Cluster(self.partition.get_membership()[n], self.scorer,records, self.scorer.analysis) for n in range(self.clusters)]
        clusters = [0] * self.nclusters

        while True:

            for n in range(self.nclusters):
                members = self.partition.get_membership()[n]
                if not clusters[n] or clusters[n].members != members:
                    clusters[n] = Cluster(members, self.scorer.records, self.scorer.analysis)


            assignment = getattr(self,self.method)(clusters)
            score = self.scorer.score(assignment)

            if score > self.L:
                self.L = score
                self.partition = assignment

            else: 
                count += 1
                if count > 1: # Algorithm is deterministic so no need for more iterations
                    break

    def distance(self,clusters): # need better name once we figure out what it does

        assignment = self.partition.partition_vector[:]
        
        for (index, record) in enumerate(self.scorer.records):
            dists = [ self.dist(record.tree, clusters[n].tree) for n in range(self.nclusters) ]
            if assignment.count(assignment[index]) > 1:
                assignment[index] = dists.index(min(dists)) + 1

        return(Partition(assignment))

    def ml(self,clusters):

        assignment = self.partition.partition_vector[:]
        
        for (index, record) in enumerate(self.scorer.records):
            likelioods = [ self.phyml_likelihood(record, clusters[n]) for n in range(self.nclusters) ]
            if assignment.count(assignment[index]) > 1:
                assignment[index] = likelioods.index(min(likelioods)) + 1

        return(Partition(assignment))

    def phyml_likelihood(self, record, cluster, verbose=0):
        p = Phyml(record, tmpdir=self.tmpdir)
        cluster.tree.write_to_file('test_tree')
        self.add_tempfile('test_tree')
        p.add_flag('--inputtree', 'test_tree') # Need tempdir????
        p.add_flag('-o', 'r') # Optimise only banch lengtha and substitutions`
        p.add_flag('-a', 'e')
        p.add_flag('-b', 0)
        p.add_flag('-c', 4)
        p.add_flag('-d', 'nt') # set data type - could inherit from Collection object?
        p.run(verbosity=verbose)

    def dist(self, tree1, tree2):
        distance = DistanceMatrix( [tree1, tree2], self.metric)[0][1] 
        return(distance)

class Cluster(object):
    def __init__(self, members, records, analysis):
        self.members = tuple(members)
        self.records = [ records[i] for i in self.members ]
        self.scorer = Scorer(records, analysis)
        self.tree = self.scorer.add(self.members)
