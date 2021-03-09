from .shared import Sourced


class Class(Sourced):
    def __init__(self, name, hit_points, proficiencies, equipment, table, levels, subclasses, optional_features,
                 feature_options,
                 **kwargs):
        """
        :type name: str
        :type hit_points: str
        :type proficiencies: str
        :type equipment: str
        :type table: ClassTable
        :type levels: list[list[ClassFeature]]
        :type subclasses: list[Subclass]
        :type optional_features: list[ClassFeature]
        :type feature_options: list[ClassFeature]
        """
        super().__init__('class', False, **kwargs)
        self.name = name
        self.hit_points = hit_points
        self.proficiencies = proficiencies
        self.equipment = equipment
        self.table = table
        self.levels = levels
        self.subclasses = subclasses
        self.optional_features = optional_features
        self.feature_options = feature_options

    @classmethod
    def from_data(cls, d):
        levels = [[] for _ in d['levels']]
        subclasses = [Subclass.from_data(s) for s in d['subclasses']]
        inst = cls(
            d['name'], d['hit_points'], d['proficiencies'], d['equipment'],
            ClassTable.from_data(d['table']), levels, subclasses, optional_features=[], feature_options=[],
            source=d['source'], entity_id=d['id'], page=d['page'], url=d['url'], is_free=d['isFree']
        )
        inst.levels = [[ClassFeature.from_data(cf, inst) for cf in lvl] for lvl in d['levels']]
        inst.optional_features = [ClassFeature.from_data(ocf, inst) for ocf in d['optional_features']]
        inst.feature_options = [ClassFeature.from_data(cfo, inst, is_class_feature_option=True)
                                for cfo in d['class_feature_options']]
        return inst


class ClassTable:
    def __init__(self, headers, levels):
        """
        :type headers: list[str]
        :type levels: list[list[str]]
        """
        if not len(levels) == 20:
            raise ValueError("Class Table must have 20 levels")
        if not all(len(lvl) == len(headers) for lvl in levels):
            raise ValueError("Number of entries in each level must equal header size")

        self.headers = headers
        self.levels = levels

    @classmethod
    def from_data(cls, d):
        return cls(
            d['headers'], d['levels']
        )


class Subclass(Sourced):
    def __init__(self, name, levels, optional_features, feature_options, **kwargs):
        """
        :type name: str
        :type levels: list[list[ClassFeature]]
        :type optional_features: list[ClassFeature]
        :type feature_options: list[ClassFeature]
        """
        super().__init__('class', False, **kwargs)
        self.name = name
        self.levels = levels
        self.optional_features = optional_features
        self.feature_options = feature_options

    @classmethod
    def from_data(cls, d):
        levels = [[] for _ in d['levels']]
        inst = cls(
            d['name'], levels, [], [],
            source=d['source'], entity_id=d['id'], page=d['page'], url=d['url'], is_free=d['isFree']
        )
        inst.levels = [[ClassFeature.from_data(cf, source_class=inst) for cf in lvl] for lvl in d['levels']]
        inst.optional_features = [ClassFeature.from_data(ocf, source_class=inst) for ocf in d['optional_features']]
        inst.feature_options = [ClassFeature.from_data(cfo, source_class=inst, is_class_feature_option=True)
                                for cfo in d['class_feature_options']]
        return inst


class ClassFeature(Sourced):
    def __init__(self, name, text, is_class_feature_option=False, **kwargs):
        entity_type = 'class-feature' if not is_class_feature_option else 'class-feature-option'
        super().__init__(entity_type, homebrew=False, **kwargs)
        self.name = name
        self.text = text

    @classmethod
    def from_data(cls, d, source_class, **kwargs):
        # noinspection PyProtectedMember
        return cls(
            d['name'], d['text'],
            entity_id=d['id'], page=d['page'],
            source=d.get('source', source_class.source), is_free=d.get('isFree', source_class.is_free),
            url=d.get('url', source_class._url),
            entitlement_entity_id=d.get('entitlementEntityId', source_class.entity_id),
            entitlement_entity_type=d.get('entitlementEntityType', 'class'),
            **kwargs
        )
