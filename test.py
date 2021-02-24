import asyncio

class Playlist(asyncio.Queue):
    async def next_song(self):
        while True:
            yield await self.get()

    async def add_song(self, song):
        await self.put(song)


class SongPlayer():
    def __init__(self):
        self.playlist = Playlist()
        self.isplaying = False

    async def add_song(self, *args, **kwargs):
        await self.playlist.add_song(*args, **kwargs)

    async def play(self):
        if not self.isplaying:
            async for song in self.playlist.next_song():
                asyncio.gather(self.play_song(song), self.input_songs())
        else:
            print("waiting for the song to finish...")

    async def play_song(self, song):
        self.is_playing()
        print('now playing:', song)
        await asyncio.sleep(5)
        print("{} has finished reproducing".format(song))
        self.is_playing()
        await self.play()

    async def add_songs(self, song):
        for song in song:
            if song != "play":
                await self.playlist.add_song(song)
                print("song {} added".format(song))
        if self.playlist.qsize() == 1:
            print("queue has one task, launching the play         function")
            asyncio.gather(self.play(), self.input_songs())


    async def input_songs(self):
        cmd = input("==>")
        if cmd.startswith("play"):
            cmd = cmd.split(" ")
            await self.add_songs(cmd)

    def is_playing(self):
        self.isplaying = not self.isplaying

loop = asyncio.get_event_loop()
player = SongPlayer()
loop.create_task(player.input_songs())
loop.run_forever()