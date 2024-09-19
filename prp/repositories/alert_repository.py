from .utils._execute_query import _execute_query

class AlertRepository:
    
    def selectAlertValidFromToDateById(self, alert_valid_from_to_date_id):
        query = '''
                SELECT * FROM CustomerRelationshipAlertValidFromToDate
                WHERE CustomerRelationshipAlertValidFromToDateId = ?
                '''
        alert_valid_from_to_date = _execute_query(query, (alert_valid_from_to_date_id,)).fetchone()
        return alert_valid_from_to_date
    
    def insertAlertValidFromToDate(self):
        query = 'INSERT INTO CustomerRelationshipAlertValidFromToDate (DateContent) VALUES (?)'
        cursor = _execute_query(query, ('',), commit=True)
        alert_valid_from_to_date_id = cursor.lastrowid
        alert_valid_from_to_date = self.selectAlertValidFromToDateById(alert_valid_from_to_date_id)
        return alert_valid_from_to_date
    
    def updateAlertValidFromToDate(self, alert_valid_from_to_date_id, body):
        query = '''
                UPDATE CustomerRelationshipAlertValidFromToDate SET DateContent = ?
                WHERE CustomerRelationshipAlertValidFromToDateId = ?
                '''
        _execute_query(query, (body.get('DateContent'), alert_valid_from_to_date_id,), commit=True)
        alert_valid_from_to_date = self.selectAlertValidFromToDateById(alert_valid_from_to_date_id)
        return alert_valid_from_to_date
    
    def selectAlertById(self, alert_id):
        query = 'SELECT * FROM Alert WHERE AlertId = ?'
        alert = _execute_query(query, (alert_id,)).fetchone()
        return alert
    
    def selectAlertByPartyStateIdAll(self, party_state_id):
        query = 'SELECT * FROM Alert WHERE PartyStateId = ?'
        alert = _execute_query(query, (party_state_id,)).fetchone()
        return alert
    
    def selectAlertByPartyStateIdAndId(self, party_state_id, alert_id):
        query = 'SELECT * FROM Alert WHERE AlertId = ? AND PartyStateId = ?'
        alert = _execute_query(query, (party_state_id, alert_id)).fetchone()
        return alert
    
    def insertAlert(self, body):
        query = '''
                INSERT INTO Alert (CustomerRelationshipAlertType,
                    CustomerRelationshipAlertNarrative,
                    CustomerRelationshipAlertValidFromToDateId,
                    PartyStateId)
                VALUES(?, ?, ?, ?)
                '''
        cursor = _execute_query(query, ('', '', body.get('CustomerRelationshipAlertValidFromToDateId'), body.get('PartyStateId'),), commit=True)
        alert_id = cursor.lastrowid
        alert = self.selectAlertById(alert_id)

        return alert
    
    def updateAlert(self, alert_id, body):
        query = '''
                UPDATE Alert SET CustomerRelationshipAlertType = ?,
                    CustomerRelationshipAlertNarrative = ?
                WHERE AlertId = ?
                '''
        _execute_query(query, (body.get('CustomerRelationshipAlertType'),
                               body.get('CustomerRelationshipAlertNarrative'),
                               alert_id,), commit=True)
        alert = self.selectAlertById(alert_id)
        return alert

    # def selectAlertByPartyStateIdAndIdAll(self, party_state_id, alert_id):
    #     query = '''
    #             SELECT Alert.AlertId, Alert.CustomerRelationshipAlertType, 
    #                 Alert.CustomerRelationshipAlertNarrative, 
    #                 CustomerRelationshipAlertValidFromToDate.CustomerRelationshipAlertValidFromToDateId,
    #                 CustomerRelationshipAlertValidFromToDate.DateContent, 
    #                 PartyState.PartyStateId, PartyState.CustomerReference
    #             FROM Alert
    #             JOIN CustomerRelationshipAlertValidFromToDate ON Alert.CustomerRelationshipAlertValidFromToDateId = CustomerRelationshipAlertValidFromToDate.CustomerRelationshipAlertValidFromToDateId
    #             JOIN PartyState ON Alert.PartyStateId = PartyState.PartyStateId
    #             WHERE Alert.PartyStateId = ?
    #             AND Alert.AlertId = ?
    #             '''
    #     alert = _execute_query(query, (party_state_id, alert_id)).fetchone()
    #     return alert