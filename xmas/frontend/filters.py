"""Frontend Jinja2 filters."""

import hashlib

__all__ = 'init_app',


def gravatar(email, size=100, rating='g', default='retro', force_default=False,
             force_lower=False, use_ssl=False):
    """Return the Gravatar image URL for an email address."""
    if use_ssl:
        domain = 'https://secure.gravatar.com'
    else:
        domain = 'http://gravatar.com'

    if force_lower:
        email = email.lower()

    email_hash = hashlib.md5(email.encode()).hexdigest()

    url = '{domain}/avatar/{hash}?s={size}&d={default}&r={rating}{force}'
    return url.format(
        domain=domain,
        hash=email_hash,
        size=size,
        default=default,
        rating=rating,
        force='&f=y' if force_default else '',
    )


def init_app(app):
    app.jinja_env.filters['gravatar'] = gravatar
