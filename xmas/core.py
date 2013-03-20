"""Application core."""

from flask.ext.mail import Mail
from flask.ext.security import Security
from flask.ext.sqlalchemy import SQLAlchemy

__all__ = 'db',


db = SQLAlchemy()  # NOQA
mail = Mail()  # NOQA
security = Security()  # NOQA


class Server(object):

    """A wrapper around common SQLAlchemy functionality."""

    def _isinstance(self, instance, raise_error=True):
        """Check if the specified instance matches the service's model.

        By default this method will raise :class:`ValueError` if the
        instance is not of the correct type.

        :param instance: the instance to check.
        :param raise_error: whether or not to raise an error on
                            type mismatch.
        :return bool: whether or not the instance is of the expected
                      type.
        :raises: ValueError

        """

        if isinstance(instance, self.__model__):
            return True
        elif raise_error:
            raise ValueError('{} is not of type {}.'.format(
                instance, self.__model__,
            ))
        else:
            return False

    def all(self):
        """Return a generator containing all instances of the model."""

        return self.__model__.query.all()

    def save(self, instance, commit=True):
        """Commit the instance to the database and return it.

        :param instance: the instance to save.
        :param commit: whether or not to commit the current session.

        """

        self._isinstance(instance)
        db.session.add(instance)
        if commit:
            db.session.commit()
        return instance
