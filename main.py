from Services.factory_pattern import Item_factory
factory = Item_factory()

for i in range(10):
    item = factory.choix_aleatoire()
    print(item.get_description())
