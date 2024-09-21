from .module import (
    SnakeyDiagram,findCode,readTraitementsData,isTreatedByItPercentage,
    yesOrNo, isTreatedByIt, isTreatedByItWithDate, isTreatedByItWithQte, 
    neoadjuvantOrAdjuvantOrBoth, chemotherapyIntervals, traitementCharacterization,
    tableSequances,tableSequancesTwo,tableValues,data,
)


# Expose the data and functions as package-level attributes
__all__ = [
    'data', 'SnakeyDiagram','findCode',
    'yesOrNo', 'isTreatedByIt', 'isTreatedByItWithDate',
    'isTreatedByItWithQte', 'neoadjuvantOrAdjuvantOrBoth', 'chemotherapyIntervals',
    'tableSequances','tableSequancesTwo','tableValues','readJSON',
    'cleanAllCodes','readTraitementsData','isTreatedByItPercentage','traitementCharacterization'
]
