import reader.songDatabase as db
import reader.songSearch as songSearch


class DataSource:

    def __init__(self, conn=db.connect()):
        self.conn = conn
        self.allSongs = db.getSavedSongsFromConnection(conn)

    # Returns a list of songs that contain the partial name
    def getSongsWithPartialName(self, partialName):
        # initial implmenentation goes to the database
        rawSongs = songSearch.getSongsFromName(partialName, self.conn)
        songs = songSearch.convertToSongObjects(rawSongs)
        return list(songs)

    def getSongsWithPartialNameMemory(self, partialName):
        # This implementation is in memory and not really working
        allSongs = list(songSearch.convertToSongObjects(db.getAllSavedSongs()))
        print("songs got")
        potentials = songSearch.getSongsWithName(allSongs, input)
        print("potentials processed lenth = " + str(len(list(potentials))))
        removeDupes = songSearch.removeDupes(potentials)
        removeDupes = list(removeDupes)
        print(removeDupes)
