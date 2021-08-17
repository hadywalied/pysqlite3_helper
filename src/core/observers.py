# from __future__ import annotations

import shlex
import subprocess
import sys
import threading
from abc import ABC, abstractmethod


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    state = None
    """
    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer) -> None:
        # print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        # print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def start_process(self, command) -> None:
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).
        """

        def target():
            self.process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            while True:
                output = self.process.stdout.readline().decode()
                if output == '' and self.process.poll() is not None:
                    self.state = 'process terminated'
                    self.notify()
                    break
                if output:
                    self.state = output
                    self.notify()

        self.thread = threading.Thread(target=target)
        self.thread.setDaemon(True)
        self.thread.start()


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""


class ConcreteObserverA(Observer):
    def update(self, subject: Subject) -> None:
        self.subject = subject
        if subject.state.__contains__('error') or subject.state.__contains__('not found') or subject.state.__contains__(
                "down"):
            print('something went wrong: {output}'.format(output=subject.state))
            sys.exit(0)
        print(subject.state)

    def __del__(self):
        if self.subject.thread.is_alive():
            self.subject.process.terminate()
            self.subject.thread.join()


if __name__ == "__main__":
    # The client code.
    # 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
    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    subject.attach(observer_a)

    subject.start_process()
    subject.start_process()

    subject.detach(observer_a)

    subject.start_process()
