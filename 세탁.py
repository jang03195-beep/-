import flet as ft
import time
import datetime

def main(page: ft.Page):
    page.title = "단국대학교 기숙사 스마트 세탁 예약"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 스마트폰 규격 크기 고정 및 여백 최적화
    page.window_width = 390
    page.window_height = 700
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # 상태 관리 변수들 (세션 유지용)
    student_id = ""
    tickets = 0  
    selected_device = None
    selected_time = None
    
    devices = {
        "세탁기 1호기": {"empty": True, "time_left": 0},
        "세탁기 2호기": {"empty": False, "time_left": 25},
        "건조기 1호기": {"empty": True, "time_left": 0},
        "건조기 2호기": {"empty": False, "time_left": 40},
    }

    def generate_timetable():
        now = datetime.datetime.now()
        timetable = []
        for i in range(1, 6):  
            future_time = now + datetime.timedelta(hours=i)
            timetable.append(future_time.strftime("%H:00"))
        return timetable

    def go_to_screen(screen_func):
        page.clean()
        screen_func()
        page.update()

    # --- 0. 단국대학교 로고 스플래시 화면 (안전 구동 방식으로 수정) ---
    def show_splash_screen():
        logo_icon = ft.Icon(ft.Icons.SCHOOL_ROUNDED, size=90, color=ft.Colors.BLUE_900)
        univ_text = ft.Text("DANKOOK UNIVERSITY", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
        sub_text = ft.Text("웅비홀 스마트 세탁 시스템", size=13, color=ft.Colors.BLUE_GREY_400, weight=ft.FontWeight.W_500)
        
        splash_container = ft.Column(
            [
                ft.Container(height=160),
                logo_icon,
                ft.Container(height=10),
                univ_text,
                sub_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            animate_opacity=800  # 부드러운 0.8초 페이드 애니메이션
        )
        
        page.add(splash_container)
        page.update()
        
        # 창이 확실히 표시된 후 페이드아웃 애니메이션 연출
        time.sleep(1.2)
        splash_container.opacity = 0.0
        page.update()
        
        time.sleep(0.8)  # 애니메이션 완료 대기
        go_to_screen(show_login_screen)

    # --- 1. 초기 진입 및 인증 화면 ---
    def show_login_screen():
        nonlocal student_id
        student_id_input = ft.TextField(
            label="학번 입력", 
            hint_text="학번 8자리를 입력하세요", 
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        def handle_login(e):
            nonlocal student_id
            if student_id_input.value:
                student_id = student_id_input.value
                page.snack_bar = ft.SnackBar(ft.Text(f"{student_id}님, 인증되었습니다."))
                page.snack_bar.open = True
                go_to_screen(show_ticket_screen)
            else:
                student_id_input.error_text = "학번을 입력해주세요."
                page.update()

        page.add(
            ft.Container(height=30),
            ft.Text("단국대 스마트 캠퍼스", size=16, color=ft.Colors.BLUE_900, weight=ft.FontWeight.BOLD),
            ft.Text("기숙사 세탁 예약 인증", size=22, weight=ft.FontWeight.BOLD),
            ft.Container(height=30),
            ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=60, color=ft.Colors.BLUE_GREY_300),
            ft.Container(height=20),
            student_id_input,
            ft.Container(height=15),
            ft.ElevatedButton(
                "학생증 인증 및 로그인", 
                on_click=handle_login, 
                width=240, 
                style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_900)
            ),
        )

    # --- 2. 서비스 준비 (티켓 구매 및 대시보드) ---
    def show_ticket_screen():
        nonlocal tickets, student_id
        ticket_text = ft.Text(f"보유 세탁 티켓: {tickets}개", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
        user_info = ft.Text(f"인증 계정: {student_id} (로그인 완료)", size=12, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD)

        def buy_ticket(count):
            nonlocal tickets
            tickets += count
            ticket_text.value = f"보유 세탁 티켓: {tickets}개"
            page.snack_bar = ft.SnackBar(ft.Text(f"세탁 티켓 {count}회권 구매가 완료되었습니다."))
            page.snack_bar.open = True
            page.update()

        def next_step(e):
            if tickets < 1:
                page.snack_bar = ft.SnackBar(ft.Text("사용 가능한 세탁 티켓이 없습니다. 먼저 구매해주세요."))
                page.snack_bar.open = True
                page.update()
            else:
                go_to_screen(show_device_screen)

        page.add(
            ft.Text("세탁 티켓 충전소", size=20, weight=ft.FontWeight.BOLD),
            user_info,
            ft.Container(height=15),
            ft.Container(
                content=ft.Column([ticket_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.BLUE_GREY_50,
                padding=15,
                border_radius=10,
                width=300
            ),
            ft.Container(height=20),
            ft.Text("티켓 상품 요금표", size=14, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton("1회권 (1,500원)", on_click=lambda e: buy_ticket(1), bgcolor=ft.Colors.BLUE_50),
                ft.ElevatedButton("3회권 (4,000원)", on_click=lambda e: buy_ticket(3), bgcolor=ft.Colors.BLUE_100),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton("5회권 (6,500원)", on_click=lambda e: buy_ticket(5), bgcolor=ft.Colors.BLUE_200),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=45),
            ft.ElevatedButton(
                "기기 선택 / 예약하러 가기 ➡️", 
                on_click=next_step, 
                bgcolor=ft.Colors.GREEN_700, 
                color=ft.Colors.WHITE,
                width=260
            ),
        )

    # --- 3. 기기 선택 및 예약 (타임테이블) ---
    def show_device_screen():
        page.add(ft.Text("기기 및 시간 예약", size=20, weight=ft.FontWeight.BOLD))
        
        device_list_view = ft.ListView(expand=False, height=220, spacing=8, padding=5)
        
        timetable_section = ft.Column(visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        timetable_title = ft.Text("", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
        time_buttons_row = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER)

        final_confirm_section = ft.Column(visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        final_confirm_text = ft.Text("", size=13, color=ft.Colors.GREEN_800, weight=ft.FontWeight.BOLD)

        def handle_device_click(device_name, is_empty):
            nonlocal selected_device, selected_time
            selected_device = device_name
            selected_time = None  
            final_confirm_section.visible = False
            
            if is_empty:
                timetable_title.value = f"⏰ [{device_name}] 예약 타임 슬롯"
                time_buttons_row.controls.clear()
                
                time_buttons_row.controls.append(
                    ft.ElevatedButton(
                        "즉시 사용", 
                        on_click=lambda e: select_time_slot("즉시"),
                        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100
                    )
                )
                
                for slot in generate_timetable():
                    time_buttons_row.controls.append(
                        ft.ElevatedButton(
                            slot, 
                            on_click=lambda e, s=slot: select_time_slot(s),
                            bgcolor=ft.Colors.GREY_200
                        )
                    )
                
                timetable_section.visible = True
                page.update()
            else:
                timetable_section.visible = False
                page.snack_bar = ft.SnackBar(ft.Text("현재 사용 중인 기기입니다. 다른 호기를 선택해 주세요."))
                page.snack_bar.open = True
                page.update()

        def select_time_slot(slot_time):
            nonlocal selected_time
            selected_time = slot_time
            if slot_time == "즉시":
                final_confirm_text.value = f"선택 완료: {selected_device} 즉시 가동"
            else:
                final_confirm_text.value = f"선택 완료: {selected_device} [{slot_time}] 예약"
            
            final_confirm_section.visible = True
            page.update()

        def start_process():
            nonlocal tickets
            tickets -= 1  
            if selected_time != "즉시":
                page.snack_bar = ft.SnackBar(ft.Text(f"⏰ [예약 알림] {selected_time} 정시 5분 전 푸시 알림 예정"))
                page.snack_bar.open = True
                page.update()
            go_to_screen(show_progress_screen)

        final_confirm_section.controls = [
            final_confirm_text,
            ft.Container(height=5),
            ft.ElevatedButton("가동 명령어 전송 🚀", on_click=lambda e: start_process(), bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE)
        ]

        timetable_section.controls = [
            ft.Divider(),
            timetable_title,
            ft.Container(height=5),
            time_buttons_row,
            final_confirm_section
        ]

        for name, info in devices.items():
            status_text = "사용 가능" if info["empty"] else f"사용 중 ({info['time_left']}분 남음)"
            status_color = ft.Colors.GREEN_700 if info["empty"] else ft.Colors.RED_600
            
            device_list_view.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Icon(ft.Icons.LOCAL_LAUNDRY_SERVICE_ROUNDED, size=24, color=ft.Colors.BLUE_900),
                            ft.Column([
                                ft.Text(name, size=14, weight=ft.FontWeight.BOLD),
                                ft.Text(status_text, size=12, color=status_color)
                            ], spacing=2)
                        ]),
                        ft.IconButton(
                            icon=ft.Icons.EVENT_AVAILABLE if info["empty"] else ft.Icons.BLOCK_ROUNDED,
                            icon_size=20,
                            icon_color=ft.Colors.BLUE_900 if info["empty"] else ft.Colors.GREY_400,
                            on_click=lambda e, n=name, em=info["empty"]: handle_device_click(n, em)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=8,
                    border=ft.Border(
                        top=ft.BorderSide(1, ft.Colors.BLACK12), bottom=ft.BorderSide(1, ft.Colors.BLACK12),
                        left=ft.BorderSide(1, ft.Colors.BLACK12), right=ft.BorderSide(1, ft.Colors.BLACK12)
                    ),
                    border_radius=8
                )
            )
        
        page.add(device_list_view)
        page.add(timetable_section)
        page.add(ft.TextButton("이전 단계(티켓충전)로 가기", on_click=lambda e: go_to_screen(show_ticket_screen)))

    # --- 4. 진행 및 완료 화면 ---
    def show_progress_screen():
        progress_bar = ft.ProgressBar(width=280, value=0.0)
        timer_text = ft.Text("서버 동기화 중...", size=16)
        next_btn = ft.ElevatedButton("확인 (원격 제어 종료)", on_click=lambda e: go_to_screen(show_end_screen), visible=False)
        
        page.add(
            ft.Text("실시간 원격 제어 현황", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Text(f"대상 기기: {selected_device}", size=14),
            ft.Text(f"설정 옵션: {selected_time}", size=14, color=ft.Colors.BLUE_900, weight=ft.FontWeight.BOLD),
            ft.Container(height=15),
            progress_bar,
            ft.Container(height=10),
            timer_text,
            ft.Container(height=20),
            next_btn
        )
        page.update()

        for i in range(1, 6):
            time.sleep(0.6)
            progress_bar.value = i / 5
            timer_text.value = f"실시간 원격 작동 중... (남은 시간 약 {5 - i}분)"
            page.update()

        timer_text.value = "🎉 가동 완료! 세탁물을 수령해 주세요."
        next_btn.visible = True
        page.update()

    # --- 5. 완료 및 루프 처리 (로그인 세션 유지 로직 반영) ---
    def show_end_screen():
        def reset_system_with_session(e):
            nonlocal selected_device, selected_time
            selected_device = None
            selected_time = None
            # 🌟 학번 인증(1단계)을 건너뛰고 곧바로 티켓 대시보드(2단계)로 이동!
            go_to_screen(show_ticket_screen)

        page.add(
            ft.Container(height=50),
            ft.Icon(ft.Icons.TASK_ALT_ROUNDED, size=80, color=ft.Colors.GREEN_600),
            ft.Container(height=20),
            ft.Text("이용 완료 안내", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("기기 이용이 안전하게 끝났습니다.", size=14),
            ft.Container(height=40),
            ft.ElevatedButton(
                "메인 화면으로 이동", 
                on_click=reset_system_with_session, 
                bgcolor=ft.Colors.BLUE_900, 
                color=ft.Colors.WHITE,
                width=220
            )
        )

    # 최초 1회만 스플래시 화면을 확실하게 송출
    show_splash_screen()

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000, host="0.0.0.0")
