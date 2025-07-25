import ttkbootstrap as ttkb
import LoginScreen as LG
import mainScreen as MS

def main():
    root = ttkb.Window()
    
    # Start with login screen
    login_screen = LG.LoginScreen(root, lambda user: MS.MainApplication(root).after_login(user))

    
    root.mainloop()

if __name__ == "__main__":
    main()