void clearDBState();

// buildAuditLogEntryFromRedisArrayReply()
void buildAuditLogEntryFromRedisArrayReply_emptyRedisReply_emptyReturn();
void buildAuditLogEntryFromRedisArrayReply_nonemptyRedisReply_auditLogEntryReturned();

// addDataFieldToAuditLogEntry()
void addDataFieldToAuditLogEntry_validDataField_dataFieldSuccessfullyAdded();

// addAuditLogEntryToList()
void addAuditLogEntryToList_emptyList_auditLogListHasNewEntryAsOnlyEntry();
void addAuditLogEntryToList_1EntryInList_auditLogListHas2EntriesIncludingNewEntryAtListTail();
void addAuditLogEntryToList_3EntriesInList_auditLogListHas4EntriesIncludingNewEntryAtListTail();

// putAuditLogEntry()
void putAuditLogEntry_entryDoesNotExistInDB_newLogEntryIsPersisted();
void putAuditLogEntry_entryExistsInDB_logEntryIsUpdatedWithNewFieldValues();

// getAuditLogEntry()
void getAuditLogEntry_doesntExistInDB_emptyAuditLogEntryIsReturned();
void getAuditLogEntry_existsInDB_entryIsReturned();

// getAllAuditLogEntriesOfUser()
void getAllAuditLogEntriesOfUser_doesntExistInDB_emptyAuditLogEntryIsReturned();
void getAllAuditLogEntriesOfUser_existsInDB_entryIsReturned();

// getAllAuditLogEntries()
void getAllAuditLogEntries_noLogsInDB_emptyResult();
void getAllAuditLogEntries_1LogInDB_1AuditLogEntriesReturned();
void getAllAuditLogEntries_3LogInDB_3AuditLogEntriesReturned();

// serializeAuditLogListToXML()
void serializeAuditLogListToXML_emptyLog_emptyLogResult();
void serializeAuditLogListToXML_1EntryInLogList_1LogEntryInXMLResult();
void serializeAuditLogListToXML_3EntriesInLogList_3LogEntriesInXMLResult();

// driver
void runAuditLogDBTests();