#include "eventDBClient.h"
#include "client.h"
#include <string.h>
#include <uuid/uuid.h>
#include "hiredis.h"
#include <assert.h>

int numFieldsInEventObject = 6;

MoneyAmount * initMoneyAmount(int dollars, int cents) {
    MoneyAmount * moneyAmount = malloc(sizeof(MoneyAmount));
    moneyAmount -> dollars = dollars;
    moneyAmount -> cents = cents;
    return moneyAmount;
}

eventObject * buildEventObject(redisReply * reply, uuid_t eventId) {
    int numElements = reply -> elements;
    assert(numElements == numFieldsInEventObject * 2);

    eventObject * e = malloc(sizeof(eventObject));
     
    char * stockSymbol = reply -> element[1] -> str;
    int dollars = atoi(reply -> element[3] -> str);
    int cents = atoi(reply -> element[5] -> str);
    enum commandType type = atoi(reply -> element[7] -> str);
    char * username = reply -> element[9] -> str;
    enum eventStatus status = atoi(reply -> element[11] -> str);
    int sizeUuid = sizeof(uuid_t);
    e -> eventId = (unsigned char *) malloc(sizeUuid);
    memset(e -> eventId, 0, sizeUuid);
    for (int i = 0; i < sizeUuid; ++i) {
        (e -> eventId)[i] = (unsigned char) eventId[i];
    }
    e -> stockSymbol = malloc(sizeof(stockSymbol));
    strcpy(e -> stockSymbol, stockSymbol);
    e -> moneyAmount = initMoneyAmount(dollars, cents);
    e -> type = type;
    e -> username = malloc(sizeof(username));
    strcpy(e -> username, username);
    e -> status = status;
    return e;
}

eventObject * buildEmptyEventObject() {
    eventObject * e = malloc(sizeof(eventObject));
    e -> eventId = NULL;
    e -> moneyAmount = malloc(sizeof(MoneyAmount));
    return e;
}

int setEvent(redisContext * c, uuid_t eventId, char * stockSymbol, MoneyAmount * targetAmount, enum commandType type, char * username) {
    if (c == NULL) {
        printf("Error: must open client connection to redis server before invoking cacheQuote()\n");
        return 0;
    }

    enum eventStatus status = PENDING;
    redisReply *reply  = redisCommand(c, "HSET %s stockSymbol %s dollars %d cents %d commandType %d username %s status %d", eventId, stockSymbol, targetAmount -> dollars, targetAmount -> cents, type, username, status);
    int result = reply -> integer == numFieldsInEventObject;
    freeReplyObject(reply);
    return result;
}

eventObject * getEvent(redisContext * c, uuid_t eventId) {
    if (c == NULL) {
        printf("Error: must open client connection to redis server before invoking cacheQuote()\n");
        return NULL;
    }

    redisReply *reply = redisCommand(c,"HGETALL %s", eventId);
    eventObject * e;
    if (reply -> elements == numFieldsInEventObject * 2) {
        e = buildEventObject(reply, eventId);
    } else {
        e = buildEmptyEventObject();
    }

    freeReplyObject(reply);
    return e;
}

void updateEventStatus(redisContext * c, uuid_t eventId, enum eventStatus status) {
    if (c == NULL) {
        printf("Error: must open client connection to redis server before invoking cacheQuote()\n");
        return;
    }

    redisReply *reply = redisCommand(c,"HSET %s status %d", eventId, status);
    freeReplyObject(reply);
    reply = redisCommand(c,"HGETALL %s", eventId);
}

void removeEvent(redisContext * c, uuid_t eventId) {
    if (c == NULL) {
        printf("Error: must open client connection to redis server before invoking cacheQuote()\n");
        return;
    }
    redisReply *reply = redisCommand(c,"DEL %s", eventId);
    freeReplyObject(reply);
}

void freeEventObject(eventObject * e) {
    if (e -> eventId == NULL) {
        free(e);
    }
    free(e -> username);
    free(e -> stockSymbol);
    free(e -> moneyAmount);
    free(e);
}