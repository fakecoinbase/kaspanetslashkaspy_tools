from kaspy_tools.utils.general_utils import hash_256
# old name:
# def loop_through_txs_hashes_list(txs_hashes_list):

class MerkleTree:
    @classmethod
    def merkle_root(cls,elements):
        def get_parent_level(elements):
            parent_level = []
            if len(elements) % 2 == 1:
                elements.append(elements[-1])
            for i in range(0, len(elements), 2):
                parent_level.append(hash_256(elements[i] + elements[i+1]))
            return parent_level

        if len(elements) == 1:
            return elements[0]

        current_level = elements.copy()
        while len(current_level) > 1:
            current_level = get_parent_level(current_level)

        return current_level[0]
