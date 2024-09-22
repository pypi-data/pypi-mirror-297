

import os
import pickle
from loguru import logger


class BaseClient:

    def __init__(self, user_acc) -> None:
        os.makedirs('./uploads', exist_ok=True)
        self._subscribers_f = os.path.join('./uploads', '{}_subscribers.pkl'.format(user_acc))

        self.subscribers_users = []
        self._load_subscribers()
 

    def _load_subscribers(self):
        if os.path.exists(self._subscribers_f):
            with open(self._subscribers_f, 'rb') as f:
                self.subscribers_users = pickle.load(f)
                logger.info(f'found {len(self.subscribers_users)} msg subscribe.')

    def remove_user_from_subscribers(self, user_address):
        if os.path.exists(self._subscribers_f):
            self.subscribers_users = [i for i in self.subscribers_users if i['user_addr'] != user_address]
            with open(self._subscribers_f, 'wb') as f:
                pickle.dump(self.subscribers_users, f)

    def add_user_to_subscribers(self, user_address, user_level=0, user_info=None):
        if len([i for i in self.subscribers_users if i['user_addr'] == user_address]) >= 1:
            pass
        else:
            if os.path.exists(self._subscribers_f):
                to_add = {
                    'user_addr': user_address,
                    'level': user_level
                }
                self.subscribers_users.append(to_add)
                with open(self._subscribers_f, 'wb') as f:
                    pickle.dump(self.subscribers_users, f)
            else:
                self.subscribers_users = []
                to_add = {
                    'user_addr': user_address,
                    'level': user_level
                }
                self.subscribers_users.append(to_add)
                with open(self._subscribers_f, 'wb') as f:
                    pickle.dump(self.subscribers_users, f)