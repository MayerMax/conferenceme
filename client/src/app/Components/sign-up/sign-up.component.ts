import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
  providers: [AuthService]
})
export class SignUpComponent implements OnInit {
  form: FormGroup;
  email = new FormControl('',[ Validators.required , Validators.email]);
  password = new FormControl('', [Validators.required, Validators.minLength(8)]);
  confirmPassword = new FormControl('', [Validators.required]);
  constructor(private fb: FormBuilder, private auth: AuthService) {
    this.form = fb.group({
      password: fb.control(null,[ Validators.required, Validators.minLength(8)]),
      confirmPassword: fb.control(null, Validators.required)
    });
    this.form.addControl('email',this.email);
  }
  getErrorConfirmMessage (){
    return this.confirmPassword.hasError('required')? 'Пароли не совпадают' : '';
  }
  getErrorEmailMessage (){
    return this.email.hasError('required')? 'Вы должны ввести значение' :
      this.email.hasError('email')? "Недействительный адрес почты" : '';
  }
  getErrorPasswordMessage(){
    return this.confirmPassword.hasError('required')? 'Пароль не может быть короче 8 символов' : '';
  }
  signUp(){
    if (this.form.valid) {
      const value =this.form.value;
      console.log('ok');
      this.auth.signUp(value.email, value.password).subscribe(
        () => {
          console.log('ok');
        }
      );
    }
  }
  ngOnInit() {
  }

}
