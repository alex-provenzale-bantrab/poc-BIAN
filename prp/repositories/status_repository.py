from .utils._execute_query import _execute_query

class StatusRepository:
    
    def selectStatusValidFromToDateById(self, status_valid_from_to_date_id):
        query = '''
                SELECT * FROM CustomerRelationshipStatusValidFromToDate
                WHERE CustomerRelationshipStatusValidFromToDateId = ?
                '''
        status_valid_from_to_date = _execute_query(query, (status_valid_from_to_date_id,)).fetchone()
        return status_valid_from_to_date
    
    def insertStatusValidFromToDate(self):
        query = 'INSERT INTO CustomerRelationshipStatusValidFromToDate (DateContent) VALUES (?)'
        cursor = _execute_query(query, ('',), commit=True)
        status_valid_from_to_date_id = cursor.lastrowid
        status_valid_from_to_date = self.selectStatusValidFromToDateById(status_valid_from_to_date_id)
        return status_valid_from_to_date
    
    def updateStatusValidFromToDate(self, status_valid_from_to_date_id, body):
        query = '''
                UPDATE CustomerRelationshipStatusValidFromToDate SET DateContent = ?
                WHERE CustomerRelationshipStatusValidFromToDateId = ?
                '''
        _execute_query(query, (body.get('DateContent'), status_valid_from_to_date_id,), commit=True)
        status_valid_from_to_date = self.selectStatusValidFromToDateById(status_valid_from_to_date_id)
        return status_valid_from_to_date
    
    def selectStatusById(self, status_id):
        query = 'SELECT * FROM Status WHERE StatusId = ?'
        status = _execute_query(query, (status_id,)).fetchone()
        return status
    
    def selectStatusByPartyStateIdAll(self, party_state_id):
        query = 'SELECT * FROM Status WHERE PartyStateId = ?'
        status = _execute_query(query, (party_state_id,)).fetchone()
        return status
    
    def selectStatusByPartyStateIdAndId(self, party_state_id, status_id):
        query = 'SELECT * FROM Status WHERE StatusId = ? AND PartyStateId = ?'
        status = _execute_query(query, (party_state_id, status_id)).fetchone()
        return status
    
    def insertStatus(self, body):
        query = '''
                INSERT INTO Status (CustomerRelationshipStatusType,
                    CustomerRelationshipStatusNarrative,
                    CustomerRelationshipStatusValidFromToDateId,
                    PartyStateId)
                VALUES(?, ?, ?, ?)
                '''
        cursor = _execute_query(query, ('', '', body.get('CustomerRelationshipStatusValidFromToDateId'), body.get('PartyStateId'),), commit=True)
        status_id = cursor.lastrowid
        status = self.selectStatusById(status_id)

        return status
    
    def updateStatus(self, status_id, body):
        query = '''
                UPDATE Status SET CustomerRelationshipStatusType = ?,
                    CustomerRelationshipStatusNarrative = ?
                WHERE StatusId = ?
                '''
        _execute_query(query, (body.get('CustomerRelationshipStatusType'),
                               body.get('CustomerRelationshipStatusNarrative'),
                               status_id,), commit=True)
        status = self.selectStatusById(status_id)
        return status