# @QueryHandler

```java
@QueryHandler
Single<DemoView> query(DemoViewFindByIdQuery query, QueryMessage<DemoViewFindByIdQuery> queryMessage) {
	Utils.logMethodFlow(this, "query", query, "BEGIN");
	var result = demoMongoRepository.findById(query.getDemoId())
			.filter(d -> d.getDeletedAt() != null)
			.map(DemoMongo::toDemoView).orElseThrow();
	Utils.logMethodFlow(this, "query", query, "END");
	return Single.of(result);
}

@QueryHandler
Multiple<DemoView> query(DemoViewFindAllQuery query) {
	Utils.logMethodFlow(this, "query", query, "BEGIN");
	var result = demoMongoRepository.findAll().stream()
			.filter(d -> d.getDeletedAt() != null)
			.map(DemoMongo::toDemoView).toList();
	Utils.logMethodFlow(this, "query", query, "END");
	return Multiple.of(result);
}

@QueryHandler
Single<DemoRichView> queryRich(DemoRichViewFindByIdQuery query) {
	Utils.logMethodFlow(this, "query", query, "BEGIN");
	var result = demoMongoRepository.findById(query.getDemoId())
			.map(DemoMongo::toDemoRichView).orElseThrow();
	Utils.logMethodFlow(this, "query", query, "END");
	return Single.of(result);
}

```
