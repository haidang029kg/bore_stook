
from Book_Flask.models import OrderDetails, Rules
from Book_Flask import db
import os
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

#source https://github.com/asaini/Apriori
def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)
                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def runApriori(minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList()
    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport
    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            """local function which Returns the support of an item"""
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in largeSet.items():
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if round(confidence,2) >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in items:
        print ("item: %s ; %.3f" % (str(item), support))
    print ("\n------------------------ RULES:")
    for rule, confidence in rules:
        pre, post = rule
        print ("Rule: %s ==> %s ; %.3f" % (str(pre), str(post), confidence))

def getItemSetTransactionList():
    data = db.session.query(OrderDetails.OrderID, OrderDetails.BookID).order_by(OrderDetails.OrderID.asc()).all()
    itemSet = set()
    tranList = list()
    tempArray = []
    curOrderID = data[0][0]  # first OrderID
    for row in data:
        itemSet.add(frozenset([row[1]]))
        if (curOrderID != row[0]):
            tranList.append(frozenset(tempArray))
            tempArray = [row[1]]
            curOrderID = row[0]
        else:
            tempArray.append(row[1])
    tranList.append(tempArray)
    return itemSet, tranList

def saveRules(rules):
    db.session.execute('DELETE FROM rules;')
    Rules_data = []
# <<<<<<< HEAD:assoRule.py
#     for i in range(0,len(rules)):
#         Rules_data.append(Rules(RID = i+1, Antecendents = str(rules[i][0][0]).strip('(),'), 
#     	                    Consequents = str(rules[i][0][1]).strip('(),'),
#     	                    Confidence = rules[i][1]))
# =======
    for i in range(0, len(rules)):
        # modified to fit the database
        temp = str(rules[i][0][0]).strip('(),')
        temp = temp.replace(' ', '')
        #######################################
        Rules_data.append(Rules(RID=i+1, Antecendents=temp,
                            Consequents=str(rules[i][0][1]).strip('(),'),
                            Confidence=rules[i][1]))

    try:
        num = db.session.query(Rules).delete()
        db.session.commit()
    except:
        db.session.rollback()
        
# >>>>>>> master:Book_Flask/admin/assoRule.py
    db.session.add_all(Rules_data)
    db.session.commit()
    db.session.close()
