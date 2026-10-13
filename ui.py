"""
Indian Traffic Rush — UI Module
Member 4: UI / Testing

Manages user interface rendering:
- Indian-themed Main Menu with title, subtitle, panel buttons, and instructions
- Real-time in-game HUD (Score, Coins, Nitro meter and percentage)
- High-contrast Game Over screen with score, coin summary, and restart buttons
"""

import pygame


class UI:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initialize fonts (using Pygame system fonts with built-in fallbacks)
        pygame.font.init()
        self.font_huge = pygame.font.SysFont("arial", 40, bold=True)
        self.font_title = pygame.font.SysFont("arial", 32, bold=True)
        self.font_subtitle = pygame.font.SysFont("arial", 16, bold=False)
        self.font_medium = pygame.font.SysFont("arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("arial", 15)
        self.font_btn = pygame.font.SysFont("arial", 18, bold=True)
        self.font_hud = pygame.font.SysFont("arial", 18, bold=True)

        # Indian Street Racing Color Palette
        self.color_white = (248, 250, 252)
        self.color_saffron = (255, 153, 51)
        self.color_orange_btn = (234, 88, 12)
        self.color_green = (19, 136, 8)
        self.color_gold = (250, 204, 21)
        self.color_cyan = (6, 182, 212)
        self.color_red = (239, 68, 68)
        self.color_panel_bg = (15, 23, 42)
        self.color_panel_border = (51, 65, 85)
        self.color_text_muted = (148, 163, 184)

    def draw_menu(self, surface: pygame.Surface):
        """
        Render the Main Menu state.
        Displays:
        - Title: INDIAN / TRAFFIC RUSH
        - Subtitle: 'Dodge Traffic. Collect Coins. Boost Your Ride.'
        - Button Panel: [ START GAME ] and 'Press SPACE to Start'
        - Instructions Panel with clear key bindings
        """
        # Semi-transparent backdrop overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((10, 14, 26, 215))
        surface.blit(overlay, (0, 0))

        center_x = self.screen_width // 2

        # 1. Indian Tricolor Accent Dots
        dot_y = 70
        dot_spacing = 16
        pygame.draw.circle(surface, self.color_saffron, (center_x - dot_spacing, dot_y), 5)
        pygame.draw.circle(surface, self.color_white, (center_x, dot_y), 5)
        pygame.draw.circle(surface, self.color_green, (center_x + dot_spacing, dot_y), 5)

        # 2. Main Title: INDIAN TRAFFIC RUSH
        title1 = self.font_huge.render("INDIAN", True, self.color_saffron)
        title1_rect = title1.get_rect(center=(center_x, 115))
        surface.blit(title1, title1_rect)

        title2 = self.font_huge.render("TRAFFIC RUSH", True, self.color_saffron)
        title2_rect = title2.get_rect(center=(center_x, 160))
        surface.blit(title2, title2_rect)

        # 3. Subtitle
        sub_text = "Dodge Traffic. Collect Coins. Boost Your Ride."
        sub_surf = self.font_subtitle.render(sub_text, True, self.color_text_muted)
        sub_rect = sub_surf.get_rect(center=(center_x, 205))
        surface.blit(sub_surf, sub_rect)

        # 4. [ START GAME ] Button Panel
        btn_w = 260
        btn_h = 48
        btn_rect = pygame.Rect(center_x - btn_w // 2, 260, btn_w, btn_h)
        pygame.draw.rect(surface, self.color_orange_btn, btn_rect, border_radius=8)
        pygame.draw.rect(surface, self.color_saffron, btn_rect, width=2, border_radius=8)

        start_btn_text = self.font_btn.render("[ START GAME ]", True, self.color_white)
        start_btn_rect = start_btn_text.get_rect(center=btn_rect.center)
        surface.blit(start_btn_text, start_btn_rect)

        # Prompt caption below button
        prompt_surf = self.font_small.render("Press SPACE to Start", True, self.color_gold)
        prompt_rect = prompt_surf.get_rect(center=(center_x, 325))
        surface.blit(prompt_surf, prompt_rect)

        # 5. Instructions Panel Box
        panel_w = 380
        panel_h = 220
        panel_rect = pygame.Rect(center_x - panel_w // 2, 370, panel_w, panel_h)
        # Background card
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((15, 23, 42, 230))
        surface.blit(panel_surf, panel_rect.topleft)
        pygame.draw.rect(surface, self.color_panel_border, panel_rect, width=2, border_radius=10)

        # Panel Header
        inst_header = self.font_medium.render("CONTROLS & INSTRUCTIONS", True, self.color_saffron)
        inst_header_rect = inst_header.get_rect(center=(center_x, 400))
        surface.blit(inst_header, inst_header_rect)

        # Divider line
        pygame.draw.line(surface, self.color_panel_border, (panel_rect.left + 20, 422), (panel_rect.right - 20, 422), 1)

        # Instructions Lines
        lines = [
            ("SPACE / ENTER", "START GAME"),
            ("A / D or ARROW KEYS", "STEER"),
            ("HOLD SPACE", "NITRO BOOST"),
            ("ESC", "RETURN TO MENU"),
        ]

        start_line_y = 445
        for idx, (key_label, action_label) in enumerate(lines):
            y_pos = start_line_y + idx * 30
            # Key pill
            key_surf = self.font_small.render(key_label, True, self.color_white)
            surface.blit(key_surf, (panel_rect.left + 25, y_pos))

            dash_surf = self.font_small.render("-", True, self.color_text_muted)
            surface.blit(dash_surf, (panel_rect.left + 225, y_pos))

            # Action label
            act_surf = self.font_small.render(action_label, True, self.color_gold if "START" in action_label or "NITRO" in action_label else self.color_text_muted)
            surface.blit(act_surf, (panel_rect.left + 245, y_pos))

    def draw_hud(
        self,
        surface: pygame.Surface,
        score: int,
        coins: int,
        nitro_pct: float,
        level: int = 1,
        banner_text: str = "",
        banner_timer: float = 0.0,
        police_active: bool = False,
        police_status: str = "",
        police_notification_timer: float = 0.0,
        police_notification_text: str = ""
    ):
        """
        Render the in-game HUD during PLAYING state.
        Displays in real time without blocking the player, road, or traffic:
        - Top-Left: SCORE: XXXX
        - Top-Center: LEVEL: X & POLICE CHASE status
        - Top-Right: COINS: XX
        - Bottom-Center: NITRO: XX% with progress bar
        - Level Transition Banner: "LEVEL X" popup for ~1 second
        - Police Chase Warning Banner: "POLICE CHASE!" popup for ~1.5 seconds
        """
        # 1. Top-Left Score Card
        score_bg = pygame.Rect(14, 12, 130, 32)
        card_surf = pygame.Surface((score_bg.width, score_bg.height), pygame.SRCALPHA)
        card_surf.fill((15, 23, 42, 200))
        surface.blit(card_surf, score_bg.topleft)
        pygame.draw.rect(surface, (51, 65, 85), score_bg, width=1, border_radius=6)

        score_text = self.font_hud.render(f"SCORE: {int(score)}", True, self.color_white)
        surface.blit(score_text, (score_bg.x + 10, score_bg.y + 6))

        # 2. Top-Center Difficulty Level Card
        level_w = 110
        level_bg = pygame.Rect((self.screen_width - level_w) // 2, 12, level_w, 32)
        card_level = pygame.Surface((level_bg.width, level_bg.height), pygame.SRCALPHA)
        card_level.fill((15, 23, 42, 200))
        surface.blit(card_level, level_bg.topleft)
        pygame.draw.rect(surface, self.color_saffron, level_bg, width=1, border_radius=6)

        level_text = self.font_hud.render(f"LEVEL: {level}", True, self.color_saffron)
        level_rect = level_text.get_rect(center=level_bg.center)
        surface.blit(level_text, level_rect)

        # 2b. Police Chase Status Indicator (Just below Level badge when active)
        if police_active:
            pol_w = 146
            pol_h = 24
            pol_x = (self.screen_width - pol_w) // 2
            pol_y = 48
            pol_bg = pygame.Rect(pol_x, pol_y, pol_w, pol_h)

            card_pol = pygame.Surface((pol_w, pol_h), pygame.SRCALPHA)
            card_pol.fill((15, 23, 42, 215))
            surface.blit(card_pol, pol_bg.topleft)

            if police_status == "FAR":
                status_color = self.color_cyan
                status_label = "POLICE: FAR"
            elif police_status == "CLOSE":
                status_color = self.color_gold
                status_label = "POLICE: CLOSE"
            else:
                status_color = self.color_red
                status_label = "POLICE: DANGER!"

            pygame.draw.rect(surface, status_color, pol_bg, width=1, border_radius=5)
            pol_text = self.font_small.render(status_label, True, status_color)
            pol_rect = pol_text.get_rect(center=pol_bg.center)
            surface.blit(pol_text, pol_rect)

        # 3. Top-Right Coins Card
        coin_bg = pygame.Rect(self.screen_width - 134, 12, 120, 32)
        card_coin = pygame.Surface((coin_bg.width, coin_bg.height), pygame.SRCALPHA)
        card_coin.fill((15, 23, 42, 200))
        surface.blit(card_coin, coin_bg.topleft)
        pygame.draw.rect(surface, (51, 65, 85), coin_bg, width=1, border_radius=6)

        coin_text = self.font_hud.render(f"COINS: {coins}", True, self.color_gold)
        surface.blit(coin_text, (coin_bg.x + 12, coin_bg.y + 6))

        # 4. Short Visual Level-Up Notification Banner (~1 second)
        if banner_timer > 0.0 and banner_text:
            banner_w = 180
            banner_h = 42
            banner_bg = pygame.Rect((self.screen_width - banner_w) // 2, 120, banner_w, banner_h)
            b_surf = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
            b_surf.fill((15, 23, 42, 220))
            surface.blit(b_surf, banner_bg.topleft)
            pygame.draw.rect(surface, self.color_gold, banner_bg, width=2, border_radius=8)

            b_text = self.font_medium.render(banner_text, True, self.color_gold)
            b_rect = b_text.get_rect(center=banner_bg.center)
            surface.blit(b_text, b_rect)

        # 4b. Police Chase Warning Banner ("POLICE CHASE!" for ~1.5 seconds)
        if police_notification_timer > 0.0 and police_notification_text:
            p_ban_w = 230
            p_ban_h = 44
            p_ban_bg = pygame.Rect((self.screen_width - p_ban_w) // 2, 175, p_ban_w, p_ban_h)
            p_surf = pygame.Surface((p_ban_w, p_ban_h), pygame.SRCALPHA)
            p_surf.fill((15, 23, 42, 235))
            surface.blit(p_surf, p_ban_bg.topleft)
            pygame.draw.rect(surface, self.color_red, p_ban_bg, width=2, border_radius=8)

            # Procedural red and blue alert indicators
            pygame.draw.circle(surface, (239, 68, 68), (p_ban_bg.left + 16, p_ban_bg.centery), 5)
            pygame.draw.circle(surface, (59, 130, 246), (p_ban_bg.right - 16, p_ban_bg.centery), 5)

            p_text = self.font_medium.render(police_notification_text, True, self.color_white)
            p_rect = p_text.get_rect(center=p_ban_bg.center)
            surface.blit(p_text, p_rect)

        # 5. Bottom Nitro Card & Gauge
        bar_w = 160
        bar_h = 14
        pct_int = int(round(max(0.0, min(1.0, nitro_pct)) * 100))

        # Overall Nitro Box
        box_w = 260
        box_h = 32
        box_x = (self.screen_width - box_w) // 2
        box_y = self.screen_height - 40

        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((15, 23, 42, 220))
        surface.blit(box_surf, (box_x, box_y))
        pygame.draw.rect(surface, (51, 65, 85), (box_x, box_y, box_w, box_h), width=1, border_radius=6)

        # Nitro Label with percentage
        nitro_label = self.font_small.render(f"NITRO: {pct_int}%", True, self.color_cyan)
        surface.blit(nitro_label, (box_x + 10, box_y + 8))

        # Nitro Bar
        bar_x = box_x + 90
        bar_y = box_y + 9
        # Background track
        pygame.draw.rect(surface, (30, 41, 59), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        # Active fill
        fill_w = int(bar_w * max(0.0, min(1.0, nitro_pct)))
        if fill_w > 0:
            pygame.draw.rect(surface, self.color_cyan, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
        # Border
        pygame.draw.rect(surface, (148, 163, 184), (bar_x, bar_y, bar_w, bar_h), width=1, border_radius=4)

    def draw_game_over(self, surface: pygame.Surface, final_score: int, coins: int, caught_by_police: bool = False):
        """
        Render the Game Over screen overlay.
        Displays:
        - Title: GAME OVER (plus CAUGHT BY POLICE if caught)
        - Stats: FINAL SCORE: XXXX, COINS COLLECTED: XX
        - Buttons: [ RESTART ] (R) and [ MAIN MENU ] (ESC)
        """
        # Semi-transparent dark overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((15, 23, 42, 225))
        surface.blit(overlay, (0, 0))

        center_x = self.screen_width // 2

        # Card Panel
        card_w = 360
        card_h = 360
        card_rect = pygame.Rect(center_x - card_w // 2, 170, card_w, card_h)

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card_surf.fill((20, 27, 45, 240))
        surface.blit(card_surf, card_rect.topleft)
        pygame.draw.rect(surface, (239, 68, 68), card_rect, width=2, border_radius=12)

        # 1. GAME OVER Title
        title_y = 210 if caught_by_police else 220
        title_surf = self.font_huge.render("GAME OVER", True, self.color_red)
        title_rect = title_surf.get_rect(center=(center_x, title_y))
        surface.blit(title_surf, title_rect)

        # Optional "CAUGHT BY POLICE!" badge
        divider_y = 255
        if caught_by_police:
            caught_text = self.font_small.render("[ CAUGHT BY POLICE! ]", True, self.color_gold)
            caught_rect = caught_text.get_rect(center=(center_x, 240))
            surface.blit(caught_text, caught_rect)
            divider_y = 260

        # Decorative divider
        pygame.draw.line(surface, (51, 65, 85), (card_rect.left + 30, divider_y), (card_rect.right - 30, divider_y), 1)

        # 2. Final Score Display
        score_surf = self.font_medium.render(f"FINAL SCORE: {int(final_score)}", True, self.color_white)
        score_rect = score_surf.get_rect(center=(center_x, 290))
        surface.blit(score_surf, score_rect)

        # 3. Coins Collected Display
        coins_surf = self.font_medium.render(f"COINS COLLECTED: {coins}", True, self.color_gold)
        coins_rect = coins_surf.get_rect(center=(center_x, 330))
        surface.blit(coins_surf, coins_rect)

        # 4. [ RESTART ] Button Panel
        btn_r_rect = pygame.Rect(center_x - 110, 380, 220, 42)
        pygame.draw.rect(surface, self.color_orange_btn, btn_r_rect, border_radius=8)
        pygame.draw.rect(surface, self.color_saffron, btn_r_rect, width=2, border_radius=8)

        r_text = self.font_btn.render("[ RESTART ]  (R)", True, self.color_white)
        r_rect = r_text.get_rect(center=btn_r_rect.center)
        surface.blit(r_text, r_rect)

        # 5. [ MAIN MENU ] Button Panel
        btn_m_rect = pygame.Rect(center_x - 110, 436, 220, 42)
        pygame.draw.rect(surface, (30, 41, 59), btn_m_rect, border_radius=8)
        pygame.draw.rect(surface, self.color_panel_border, btn_m_rect, width=2, border_radius=8)

        m_text = self.font_btn.render("[ MAIN MENU ]  (ESC)", True, self.color_white)
        m_rect = m_text.get_rect(center=btn_m_rect.center)
        surface.blit(m_text, m_rect)
