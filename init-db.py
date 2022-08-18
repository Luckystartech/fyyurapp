from app import db, Venue, Artist, Show
# from models import db, Venue, Artist, Show

# POPULATE Venue table
Venue1 = Venue(
    id = 1,
    name = 'The Musical Hop',
    genres = ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
    city = 'San Francisco',
    state = 'CA',
    address = '1015 Folsom Street',
    phone = '123-123-1234',
    website = 'https://www.themusicalhop.com',
    image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    facebook_link = 'https://www.facebook.com/TheMusicalHop',
    seeking_talent = True,
    seeking_description = 'We are on the lookout for a local artist to play every two weeks. Please call us.'
    )

Venue2 = Venue(
    id = 2,
    name = 'The Dueling Pianos Bar',
    genres = ["Classical", "R&B", "Hip-Hop"],
    city = 'New York',
    state = 'NY',
    address = '335 Delancey Street',
    phone = '914-003-1132',
    website = 'https://www.theduelingpianos.com',
    image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    facebook_link = 'https://www.facebook.com/theduelingpianos',
    seeking_talent = False,
    seeking_description = 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
    )

Venue3 = Venue(
    id = 3,
    name = 'Park Square Live Music & Coffee',
    genres = ["Rock n Roll", "Jazz", "Classical", "Folk"],
    city = 'San Francisco',
    state = 'CA',
    address = '34 Whiskey Moore Ave',
    phone = '415-000-1234',
    website = 'https://www.parksquarelivemusicandcoffee.com',
    image_link = 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    facebook_link = 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
    seeking_talent = False,
    )  

# POPULATE Artist table
Artist1 = Artist(
    id = 4,
    name = 'Guns N Petals',
    city = 'San Francisco',
    state = 'CA',
    phone = '326-123-5000',
    website = 'https://www.gunsnpetalsband.com',
    genres = ["Rock n Roll"],
    image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    facebook_link = 'https://www.facebook.com/GunsNPetals',
    seeking_venue = True,
    seeking_description = 'Looking for shows to perform at in the San Francisco Bay Area!'
    )

Artist2 = Artist(
    id = 5,
    name = 'Matt Quevedo',
    city = 'New York',
    state = 'NY',
    phone = '300-400-5000',
    genres = ["Jazz"],
    image_link = 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    facebook_link = 'https://www.facebook.com/mattquevedo923251523',
    seeking_venue = False,
    )

Artist3 = Artist(
    id = 6,
    name = 'The Wild Sax Band',
    city = 'San Francisco',
    state = 'CA',
    phone = '432-325-5432',
    genres = ["Jazz"],
    image_link = 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    seeking_venue = False,
    )


# POPULATE Shows table
show1 = Show(
    venue_id = 1,
    # venue_name = 'The Musical Hop',
    artist_id = 4,
    # artist_name = 'Guns N Petals',
    # artist_image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    start_time = '2019-05-21T21:30:00.000Z'
)

show2 = Show(
    venue_id = 3,
    # venue_name = 'Park Square Live Music & Coffee',
    artist_id = 5,
    # artist_name = 'Matt Quevedo',
    # artist_image_link = 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    start_time = '2019-06-15T23:00:00.000Z'
)

show3 = Show(
    venue_id = 3,
    # venue_name = 'Park Square Live Music & Coffee',
    artist_id = 6,
    # artist_name = 'The Wild Sax Band',
    # artist_image_link = 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    start_time = '2035-04-01T20:00:00.000Z'
)

show4 = Show(
    venue_id = 3,
    # venue_name = 'Park Square Live Music & Coffee',
    artist_id = 6,
    # artist_name = 'The Wild Sax Band',
    # artist_image_link = 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    start_time = '2035-04-08T20:00:00.000Z'
)

show5 = Show(
    venue_id = 3,
    # venue_name = 'Park Square Live Music & Coffee',
    artist_id = 6,
    # artist_name = 'The Wild Sax Band',
    # artist_image_link = 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    start_time = '2035-04-15T20:00:00.000Z'
)





db.session.add_all([Venue1, Venue2, Venue3])
db.session.add_all([Artist1, Artist2, Artist3])
db.session.add_all([show1, show2, show3, show4, show5])
db.session.commit()