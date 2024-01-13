import utils

pause_button_pos = utils.PAUSE_IMAGE.get_rect()
pause_button_pos.topleft = (utils.SCREEN_WIDTH + utils.PAUSE_POSITION[0], utils.PAUSE_POSITION[1])

pause_button_pos_on_score_area = utils.PAUSE_IMAGE.get_rect()
pause_button_pos_on_score_area.topleft = (utils.PAUSE_POSITION[0], utils.PAUSE_POSITION[1])

back_button_rect = utils.BACK_IMAGE.get_rect()
back_button_rect.topleft = (utils.BACK_POSITION[0], utils.BACK_POSITION[1])

visualize_button_rect = utils.VISUALIZE_IMAGE.get_rect()
visualize_button_rect.topleft = (utils.VISUALIZE_POSITION[0], utils.VISUALIZE_POSITION[1])

save_button_pos = utils.SAVE_IMAGE.get_rect()
save_button_pos.topleft = (utils.SAVE_POSITION[0], utils.SAVE_POSITION[1])

back_button_in_rank = utils.BACK_IMAGE.get_rect()
back_button_in_rank.topleft = (utils.BACK_POSITION_IN_RANK[0], utils.BACK_POSITION_IN_RANK[1])

clear_button_in_rank = utils.CLEAR_IMAGE.get_rect()
clear_button_in_rank.topleft = (utils.CLEAR_POSITION[0], utils.CLEAR_POSITION[1])