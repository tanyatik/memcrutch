

class CarouselIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.container = []
        # Position points at the index of currently selected item in the carousel, starting from 0
        self.position = -1

    def current(self):
        """
        Return the item that the iterator is currenly pointing to.
        Unless the underlying iterator was pointing at an empty collection,
        this is guaranteed to return a valid element.
        """
        print(f"current() now position is {self.position}")
        if self.position == -1:
            # No current result yet,
            # this can happen only after initialising the container
            # Calling next() to initialise the container
            return self.next()

        assert 0 <= self.position < len(self.container), "self.position is out of bounds, indicating a bug"
        return self.container[self.position]

    def next(self):
        self.position += 1
        print(f"next() now position is {self.position}")

        if len(self.container) - 1 < self.position:
            try:
                self.container.append(next(self.iterator))
            except StopIteration as e:
                # If we have reached the end, decrement the position back to be the last valid one
                self.position -= 1
                print(f"next() reached the end, position is {self.position}")
                raise e

        return self.current()

    def previous(self):
        self.position -= 1
        print(f"previous() now position is {self.position}")

        if self.position < 0:
            # If we have reached the end, increment the position back to be the last valid one
            self.position += 1
            print(f"previous() reached the end, position is {self.position}")
            raise StopIteration()

        return self.current()