from helpers import surroundingGraphviz
import unittest


TEST_CURSOR = 119

TEST_CODE = '''digraph {
subgraph cluster_small {
a -> b; label=small;
}
subgraph cluster_big {
p -> q -> r -> s -> t;
label=big;
t -> p;
}
t -> a; b -> q;
}'''
TEST_SOURCE = '''
## my test

```graphviz
''' + TEST_CODE + '''
```

## stage

deploy new VMs
deploy new stage proxy to new VMs

## production
deploy new production proxy to VMs

-- dot -Tpdf -otutorial.pdf
'''


class TestSurroundingGraphviz(unittest.TestCase):
    def test_valid_code(self):
        self.assertEqual(surroundingGraphviz(TEST_SOURCE, TEST_CURSOR), TEST_CODE)


if __name__ == '__main__':
    unittest.main()


