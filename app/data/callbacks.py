from aiogram.utils.callback_data import CallbackData

base_cb = CallbackData('post', 'option', 'page', sep='|')
""">>> ('option', 'page')"""

ext_cb = CallbackData('post', 'option', 'page', 'data', sep='|')
""">> ('option', 'page', 'data')"""
