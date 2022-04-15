from .. import AfrTestManager as afr_tm

def test_processResultsSingleFreq():
    data = [[{100 : {'amplitude' : [1.0, 1.5, 2.0]}}, 1.5], 
            [{100 : {'amplitude' : [10.0, 15, 20, 14, 12]}}, 14],
            [{100 : {'amplitude' : [1.0, 1.5, 1.4, 2.0]}}, 1.45],
            [{100 : {'amplitude' : [1.0, 1.5, 1.5, 2.0]}}, 1.5]]

    dut = afr_tm.AfrTestManager(44100)
    for i in data:
        result = dut.processResults(i[0])
        assert result[100] == i[1]


def test_processResultsSingleAmplitude():
    data = {50 : {'amplitude' : [1.4]},
            200 : {'amplitude' : [14]},
            1000 : {'amplitude' : [0.0]}}

    dut = afr_tm.AfrTestManager(44100)
    result = dut.processResults(data)
    assert result[50] == 1.4
    assert result[200] == 14
    assert result[1000] == 0.0