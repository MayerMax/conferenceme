import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  providers: [AuthService]
})
export class LoginComponent implements OnInit {
  form: FormGroup;
  email = new FormControl('',[ Validators.required , Validators.email]);
  constructor(private fb: FormBuilder,private router: Router, private auth: AuthService) {
  }
  ngOnInit() {
    this.form = this.fb.group(
      {
        password: ['', Validators.required]
      });
    this.form.addControl('email', this.email);
  }
  getErrorMessage (){
    return this.email.hasError('required')? 'Вы должны ввести значение' :
      this.email.hasError('email')? "Недействительный адрес почты" : '';
  }
  login() {
    if (this.form.valid) {
      const value =this.form.value;
      console.log('ok');
      this.auth.login(value.email, value.password).subscribe(
        () => {
          console.log('ok');
          this.router.navigateByUrl('/');
        }
      );
    }
  }
}
