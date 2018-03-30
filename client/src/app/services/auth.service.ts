import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs/Observable";
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/publishReplay';
@Injectable()
export class AuthService {
  private BaseUrl = 'http://localhost:8080';
  constructor(private  http: HttpClient) { }
  login(email: string, password: string): Observable<any> {
    let url = `${this.BaseUrl}/login`;
    return this.http.post(url, {email, password}).do(
      res => this.setSession);
  }
  private setSession(authResult) {
    localStorage.setItem('id_token', authResult.idToken);
  }
  logout() {
    localStorage.removeItem('id_token');
  }
}
