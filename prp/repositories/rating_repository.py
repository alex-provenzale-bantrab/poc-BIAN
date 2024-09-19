from .utils._execute_query import _execute_query

class RatingRepository:
    
    def selectRatingValidFromToDateById(self, rating_valid_from_to_date_id):
        query = '''
                SELECT * FROM CustomerRelationshipRatingValidFromToDate
                WHERE CustomerRelationshipRatingValidFromToDateId = ?
                '''
        rating_valid_from_to_date = _execute_query(query, (rating_valid_from_to_date_id,)).fetchone()
        return rating_valid_from_to_date
    
    def insertRatingValidFromToDate(self):
        query = 'INSERT INTO CustomerRelationshipRatingValidFromToDate (DateContent) VALUES (?)'
        cursor = _execute_query(query, ('',), commit=True)
        rating_valid_from_to_date_id = cursor.lastrowid
        rating_valid_from_to_date = self.selectRatingValidFromToDateById(rating_valid_from_to_date_id)
        return rating_valid_from_to_date
    
    def updateRatingValidFromToDate(self, rating_valid_from_to_date_id, body):
        query = '''
                UPDATE CustomerRelationshipRatingValidFromToDate SET DateContent = ?
                WHERE CustomerRelationshipRatingValidFromToDateId = ?
                '''
        _execute_query(query, (body.get('DateContent'), rating_valid_from_to_date_id,), commit=True)
        rating_valid_from_to_date = self.selectRatingValidFromToDateById(rating_valid_from_to_date_id)
        return rating_valid_from_to_date
    
    def selectRatingById(self, rating_id):
        query = 'SELECT * FROM Rating WHERE RatingId = ?'
        rating = _execute_query(query, (rating_id,)).fetchone()
        return rating
    
    def selectRatingByPartyStateIdAll(self, party_state_id):
        query = 'SELECT * FROM Rating WHERE PartyStateId = ?'
        rating = _execute_query(query, (party_state_id,)).fetchone()
        return rating
    
    def selectRatingByPartyStateIdAndId(self, party_state_id, rating_id):
        query = 'SELECT * FROM Rating WHERE RatingId = ? AND PartyStateId = ?'
        rating = _execute_query(query, (party_state_id, rating_id)).fetchone()
        return rating
    
    def insertRating(self, body):
        query = '''
                INSERT INTO Rating (CustomerRelationshipRatingType,
                    CustomerRelationshipRatingNarrative,
                    CustomerRelationshipRatingValidFromToDateId,
                    PartyStateId)
                VALUES(?, ?, ?, ?)
                '''
        cursor = _execute_query(query, ('', '', body.get('CustomerRelationshipRatingValidFromToDateId'), body.get('PartyStateId'),), commit=True)
        rating_id = cursor.lastrowid
        rating = self.selectRatingById(rating_id)

        return rating
    
    def updateRating(self, rating_id, body):
        query = '''
                UPDATE Rating SET CustomerRelationshipRatingType = ?,
                    CustomerRelationshipRatingNarrative = ?
                WHERE RatingId = ?
                '''
        _execute_query(query, (body.get('CustomerRelationshipRatingType'),
                               body.get('CustomerRelationshipRatingNarrative'),
                               rating_id,), commit=True)
        rating = self.selectRatingById(rating_id)
        return rating