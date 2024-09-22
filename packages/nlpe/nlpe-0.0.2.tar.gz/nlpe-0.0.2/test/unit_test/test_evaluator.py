from nlpe import EvaluatorProxy
import numpy as np
    
class Evaluator:
    def dump(self):
        print("dump evaluator")
        
    def compute(self, predictions, label):
        assert len(predictions) == len(label)
        length = len(predictions)
        acc = np.sum(np.array(predictions) == np.array(label))/length
        return {
            "acc": acc,
        }
        
            
def test_evaluator_proxy():
    evaluator = Evaluator()
    proxy = EvaluatorProxy(
        glossary="evaluator_ proxy",
        compute_call= evaluator.compute
    )
    
    assert 0.33 == round(proxy.compute(predictions=[1,2,3], label=[1,1,1])["acc"],2)