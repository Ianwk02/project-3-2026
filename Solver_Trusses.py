#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:34:19 2021

@author: kendrick
"""

import numpy as np
import Classes_Trusses

# compute unknown displacements 
def ComputeDisplacements(K, F, n_unknowns):
    # extract submatrix of unknowns
    K11 = K[0:n_unknowns,0:n_unknowns]
    F1 = F[0:n_unknowns]
    
    d = np.linalg.solve(K11,F1)
    
    return d

# postprocess the forces at known displacement nodes
def PostprocessReactions(K, d, F, n_unknowns, nodes):
    # These are computed net forces and do not
    # take into account external loads applied
    # at these nodes
    F = np.matmul(K[n_unknowns:,0:n_unknowns], d)
    
    # Postprocess the reactions
    for node in nodes:
        if node.xidx >= n_unknowns:
            node.AddReactionXForce(F[node.xidx-n_unknowns][0] - node.xforce_external)
        if node.yidx >= n_unknowns:
            node.AddReactionYForce(F[node.yidx-n_unknowns][0] - node.yforce_external)
        
    return F

# determine internal member loads
def ComputeMemberForces(bars):
    for bar in bars:
        E=bar.E
        A=bar.A
        L= bar.length()
        lambda_x = bar.LambdaTerms()[0]
        lambda_y = bar.LambdaTerms()[1]
        dnx = bar.node_init.xdisp
        dny = bar.node_int.ydisp
        dfx = bar.node_end.xdisp
        dfy = bar.node_end.ydisp
        
        q_bar = ((A*E)/L)*(np.array([-lambda_x,-lambda_y,lambda_x, lambda_y])@np.array([dnx],[dny],[dfx],[dfy]))
        bar.axial_load = q_bar
   
    # COMPLETE THIS FUNCTION
    # Compute member forces for all bars using equation 14-23 
    pass
    
# compute the normal stresses
def ComputeNormalStresses(bars):
    for bar in bars:
        stress = bar.axial_load/bar.A
        
        bar.normal_stress = stress
    
    # COMPLETE THIS FUNCTION
    # Compute normal stress for all bars
    pass

# compute the critical buckling load of a member
def ComputeBucklingLoad(bars):
    for bar in bars:
        Pcr = ((np.pi**2)*bar.E*bar.Iu)/(bar.Length()**2)
        
        bar.buckling_load = Pcr
   
    # COMPLETE THIS FUNCTION
    # Compute critical buckling load for all bars
    pass
