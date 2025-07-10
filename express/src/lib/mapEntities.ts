function mapEntities<idT extends string | number, entityT extends { id: idT }>(
    entities: Array<entityT>,
) {
    return entities.reduce((acc, entity) => {
        return { ...acc, [entity.id]: entity };
    }, {} as Record<string, entityT>);
}

export { mapEntities };
