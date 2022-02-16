from django.dispatch import Signal

#: Signal that is fired when a Helmholtz AAI user logs in for the first time
aai_user_created = Signal()

#: Signal that is fired when a Helmholtz AAI user logs in
aai_user_logged_in = Signal()

#: Signal that is fired when a Helmholtz AAI user logs in and is updated
aai_user_updated = Signal()

#: Signal that is fired if a new Virtual Organization has been created
aai_vo_created = Signal()

#: Signal that is fired if a Helmholtz AAI user enteres a VO
aai_vo_entered = Signal()

#: Signal that is fired if a Helmholtz AAI user left a VO
aai_vo_left = Signal()
