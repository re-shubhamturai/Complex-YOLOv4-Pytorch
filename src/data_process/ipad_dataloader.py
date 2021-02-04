from data_process.ipad_dataset import IpadDataset
from torch.utils.data import DataLoader
def create_ipad_dataloader(ptcl, pixCoordinates, imageColor, translation_table, depthValues):
    test_dataset = IpadDataset(ptcl, pixCoordinates, imageColor, translation_table, depthValues)

    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False,
                                pin_memory=True, num_workers=1, sampler=None,
                                collate_fn=None)
    return test_dataloader